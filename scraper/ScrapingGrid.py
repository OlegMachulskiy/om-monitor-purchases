# -*- coding: utf-8 -*-
import random

import rpyc
import threading
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
            if len(self.tasks) < 10 or self.callCounter % 100 == 0:
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


class ScrapingHub(rpyc.Service):
    """
    Scraping HUB.
    """

    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        print "on_connect:", self
        self.dbSaver = DBSaver()
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        print "on_disconnect:", self
        del self.dbSaver
        pass

    def exposed_getNextTask(self):  # this is an exposed method
        print "method enter: exposed_getNextTask"
        sq = ScrapingQueue()
        rv = sq.getNextTask()
        print "method result: exposed_getNextTask", rv
        return rv

    def exposed_markTaskCompleted(self, ssid):  # this is an exposed method
        print "method enter: exposed_getNextTask", ssid
        sq = ScrapingQueue()
        sq.markTaskCompleted(ssid)

    def exposed_getDBSaver(self):
        return self.dbSaver

        # def exposed_storeHTTPProxyResul(self):


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    t = ThreadedServer(ScrapingHub, port=51715, protocol_config={"allow_public_attrs": True})

    t.start()
