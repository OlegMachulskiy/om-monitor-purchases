# -*- coding: utf-8 -*-

##############################################################################################################
### multi-threaded  runner.
##############################################################################################################
import random
import threading
import time

from scraperPurchase import *

thread_lock = threading.Lock()
vgScrapingEntities = []
vgEntitiesInProgress = set([])


class WorkerThread(threading.Thread):
    def __init__(self, workerDataFacade):
        threading.Thread.__init__(self)
        self.workerDataFacade = workerDataFacade
        self.loadScrapingEntities()

    def loadScrapingEntities(self):
        global vgScrapingEntities
        global vgDBS
        if vgScrapingEntities == None or len(
                vgScrapingEntities) < threading.active_count():
            with thread_lock:
                dbs = DBSaver()
                try:
                    vgScrapingEntities = self.workerDataFacade.getScrapingEntitiesFromDBS(
                        dbs)
                    print "vgScrapingEntities: ", len(
                        vgScrapingEntities), ":", vgScrapingEntities[:32]
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
            # if len(vgScrapingEntities) % 10 == 0:
            #     print "####Left in queue:", len(
            #         vgScrapingEntities), "threads:", threading.active_count(), "thread:", threading.current_thread
            return theObj

    def run(self):
        scrapingItem = None
        try:
            self.dbSaver = DBSaver()
            self.scraper = ScrapZakupkiGovRu()
            self.scraper.initializeWebdriver(useProxy=True)

            doRun = True
            while doRun:
                scrapingItem = WorkerThread.getScrapingEntity()
                if scrapingItem == None:
                    doRun = False
                else:
                    self.workerDataFacade.runScrapingForEntity(self.dbSaver, self.scraper,
                                                               scrapingItem)

        finally:
            if scrapingItem != None:    vgEntitiesInProgress.remove(str(scrapingItem))
            if self.scraper != None:    del self.scraper
            if self.dbSaver != None:    del self.dbSaver

    # PurchasesPostETL(vgDBS.conn).runQueriesList0(PurchasesPostETL.sqls1)
    @staticmethod
    def startScrapingEngine(workerDataFacade, threadsCount=8):
        wts = WorkerThread(workerDataFacade)
        wts.start()

        while len(vgScrapingEntities) > 0:
            time.sleep(3)
            print "Active threads:", threading.active_count(), \
                "Queue length:", len(vgScrapingEntities), \
                "currentThread:", threading.current_thread
            if threading.active_count() < threadsCount:
                with(thread_lock):
                    wts = WorkerThread(workerDataFacade)
                    wts.start()

        for t in threading.enumerate():
            if t != threading.current_thread():
                t.join()


class AbstractWorkerDataFacade:
    def getScrapingEntitiesFromDBS(self, dbSaver):
        raise Exception(
            "method getScrapingEntitiesFromDBS must be implemented in a runner class")
        # for example return dbs.getPurchases(1)

    def runScrapingForEntity(self, dbSaver, scraper, scrapingItem):
        raise Exception(
            "method runScrapingForEntity must be implemented in a runner class")
        # for example:
        # self.scraper.scrapOrderContent(self.dbSaver, scrapingItem)
        # self.dbSaver.touchPurchase(scrapingItem.purchaseId)
