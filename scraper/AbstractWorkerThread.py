# -*- coding: utf-8 -*-

##############################################################################################################
### read existing list of purchase orders and load details
##############################################################################################################
import inspect
import random
import threading
import time

from scraperPurchase import *

thread_lock = threading.Lock()
vgScrapingEntities = []
vgEntitiesInProgress = set([])


class AbstractWorkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.loadScrapingEntities()

    def loadScrapingEntities(self):
        global vgScrapingEntities
        global vgDBS
        if vgScrapingEntities == None or len(vgScrapingEntities) < threading.active_count():
            with thread_lock:
                dbs = DBSaver()
                try:
                    vgScrapingEntities = self.getScrapingEntitiesFromDBS()
                    print "vgScrapingEntities: ", len(vgScrapingEntities), ":", vgScrapingEntities[:32]
                finally:
                    del dbs

    @staticmethod
    def getScrapingEntity():
        global vgScrapingEntities
        with thread_lock:
            theObj = None
            if len(vgScrapingEntities) > 0:
                for i in range(1, 100):
                    idx = random.randint(0, len(vgScrapingEntities) - 1)
                    obj = vgScrapingEntities[idx]
                    if str(obj) not in vgEntitiesInProgress:
                        vgEntitiesInProgress.add(str(theObj))
                        vgScrapingEntities.pop(idx)
                        theObj = obj
                        break
            if len(vgScrapingEntities) % 10 == 0:
                print "####Left in queue:", len(
                    vgScrapingEntities), "threads:", threading.active_count(), "thread:", threading.current_thread
            return theObj

    def run(self):
        scrapingItem = None
        try:
            self.scraper = ScrapZakupkiGovRu('http://www.ya.ru')
            self.scraper.initializeWebdriver(useProxy=True)
            self.dbSaver = DBSaver()

            doRun = True
            while doRun:
                scrapingItem = AbstractWorkerThread.getScrapingEntity()
                if scrapingItem == None:
                    doRun = False
                else:
                    self.runScrapingForEntity(self.dbSaver, scrapingItem)

        finally:
            if scrapingItem != None:    vgEntitiesInProgress.remove(str(scrapingItem))
            if self.scraper != None:    del self.scraper
            if self.dbSaver != None:    del self.dbSaver

    def getScrapingEntitiesFromDBS(self):
        raise Exception("method getScrapingEntitiesFromDBS must be implemented in a runner class")
        # for example return dbs.getPurchases(1)

    def runScrapingForEntity(self, dbSaver, scrapingItem):
        raise Exception("method runScrapingForEntity must be implemented in a runner class")
        # for example:
        # self.scraper.scrapOrderContent(self.dbSaver, scrapingItem)
        # self.dbSaver.touchPurchase(scrapingItem.purchaseId)

    # PurchasesPostETL(vgDBS.conn).runQueriesList0(PurchasesPostETL.sqls1)
    @staticmethod
    def startScrapingEngine(vClass, threadsCount=8):
        threads = []
        if inspect.isclass(vClass):
            wts = vClass(vClass.__name__)
        else:
            print  vClass
        threads.append(wts)

        for i in range(0, len(threads)):
            threads[i].start()

        while len(vgScrapingEntities) > 0:
            time.sleep(3)
            print "Active threads:", threading.active_count(), "thread:", threading.current_thread
            if threading.active_count() < 10:
                with(thread_lock):
                    wts = vClass(vClass.__name__)
                    # wts = WorkerThread()
                    threads.append(wts)
                    wts.start()

        for t in threading.enumerate():
            if t != threading.current_thread():
                t.join()
