# -*- coding: utf-8 -*-

from scraperPurchase import *
from ScrapingTask import *
from WDFnewPurchases import *
from WDFpurchaseBids import *
from WDFpurchaseDetails import *
from WDFsbisOrganizations import *
from WDFpurchaseContracts import *


class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class ScrapingQueue(Singleton):
    tasks = {}  # printable task Id -> ScrapingTask() instance
    inProgress = {}  # printable task Id -> ScrapingTask() instance
    thrLock = threading.Lock()
    dataFacades = [WDFnewPurchases(), WDFpurchaseBids(), WDFpurchaseDetails(), WDFsbisOrganizations(),
                   WDFpurchaseContracts()]
    callCounter = 0

    def __init__(self):
        Singleton.__init__(self)

    def refreshQueue(self):
        print "refreshQueue"
        PurchasesPostETL(DBSaver().conn).runQueriesList0(PurchasesPostETL.sqls1)
        dbs = DBSaver()
        try:
            self.tasks = {}
            for df in self.dataFacades:
                sObjects = df.getScrapingEntitiesFromDBS(dbs)
                for so in sObjects:
                    key = df.getSIID(so)
                    value = ScrapingTask(so, df)
                    self.tasks[key] = value
                print "re-read tasks from ", df, ", len=", len(sObjects), ":", sObjects[:10]
        finally:
            del dbs

    def getNextTask(self):
        """
        :return: ScrapingTask object
        """
        with self.thrLock:
            self.callCounter += 1

            theObj = None
            if len(self.tasks) < 10 \
                    or (len(self.tasks) < 100 and self.callCounter % 10 == 0) \
                    or self.callCounter % 100 == 0:
                self.refreshQueue()

            if len(self.tasks) > 0:
                for i in range(1, 100):  ## 100 attempts to find element which was not in processing
                    keysArray = self.tasks.keys()
                    idx = random.randint(0, len(keysArray) - 1)
                    ssid = keysArray[idx]
                    value = self.tasks[ssid]
                    if ssid not in self.inProgress:
                        self.inProgress[ssid] = value
                        self.tasks.pop(ssid)
                        theObj = value
                        break
            print "Returning:", theObj, "progress=", self.inProgress.keys()
            return theObj

    def markTaskCompleted(self, ssid):
        with self.thrLock:
            print " TRY TO POP ", ssid, ", progress=", self.inProgress.keys()
            self.inProgress.pop(ssid)

    def getLength(self):
        if self.tasks is None:
            return 0
        else:
            return len(self.tasks)

    def getProgress(self):
        return self.inProgress
