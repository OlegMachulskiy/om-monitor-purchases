# -*- coding: utf-8 -*-

##############################################################################################################
### multi-threaded  runner.
##############################################################################################################
import random
import threading
import time
import traceback
from dircache import reset

from scraperPurchase import *
import sys

thread_lock = threading.Lock()
global vgScrapingEntities
global vgEntitiesInProgress

vgScrapingEntities = []
vgEntitiesInProgress = set()


class WorkerThread(threading.Thread):
    def __init__(self, workerDataFacade):
        threading.Thread.__init__(self)
        self.workerDataFacade = workerDataFacade
        self.loadScrapingEntities()

    def loadScrapingEntities(self):
        global vgScrapingEntities
        if vgScrapingEntities == None or len(
                vgScrapingEntities) < threading.active_count():
            with thread_lock:
                dbs = DBSaver()
                try:
                    vgScrapingEntities = self.workerDataFacade.getScrapingEntitiesFromDBS(dbs)
                    print "vgScrapingEntities: ", len(
                        vgScrapingEntities), ":", vgScrapingEntities[:32]
                finally:
                    del dbs

    @staticmethod
    def getScrapingEntity(workerDataFacade):
        global vgScrapingEntities
        global vgEntitiesInProgress
        with thread_lock:
            theObj = None
            if len(vgScrapingEntities) > 0:
                for i in range(1, 100):
                    idx = random.randint(0, len(vgScrapingEntities) - 1)
                    obj = vgScrapingEntities[idx]
                    if workerDataFacade.getSIID(obj) not in vgEntitiesInProgress:
                        vgEntitiesInProgress.add(workerDataFacade.getSIID(obj))
                        vgScrapingEntities.pop(idx)
                        theObj = obj
                        break
            # if len(vgScrapingEntities) % 10 == 0:
            #     print "####Left in queue:", len(
            #         vgScrapingEntities), "threads:", threading.active_count(), "thread:", threading.current_thread
            return theObj

    def run(self):
        global vgScrapingEntities
        global vgEntitiesInProgress

        try:

            dbSaver = DBSaver()
            doRun = True

            proxyAddr = None
            current_milli_time = int(round(time.time() * 1000))
            while doRun:
                scrapingItem = WorkerThread.getScrapingEntity(self.workerDataFacade)
                current_milli_time = int(round(time.time() * 1000))
                if scrapingItem == None:
                    doRun = False
                    break
                else:
                    scraper = None
                    try:
                        scraper = ScrapZakupkiGovRu()
                        proxyAddr = scraper.initializeWebdriver(useProxy=True)
                        self.workerDataFacade.runScrapingForEntity(dbSaver, scraper,
                                                                   scrapingItem)

                        dbSaver.storeHTTPProxyResult(proxyAddr, int(round(time.time() * 1000)) - current_milli_time,
                                                     "Success")
                    finally:
                        if scraper != None:    del scraper
                        if scrapingItem != None:
                            vgEntitiesInProgress.remove(self.workerDataFacade.getSIID(scrapingItem))

        except Exception as ex:
            dbSaver.storeHTTPProxyResult(proxyAddr, int(round(time.time() * 1000)) - current_milli_time, str(ex))
            dbSaver.logErr("Failure", ex)
            raise ex
        finally:
            if dbSaver != None:
                del dbSaver

    # PurchasesPostETL(vgDBS.conn).runQueriesList0(PurchasesPostETL.sqls1)
    @staticmethod
    def startScrapingEngine(workerDataFacade, threadsCount=8):
        global vgScrapingEntities
        global vgEntitiesInProgress

        wts = WorkerThread(workerDataFacade)
        wts.start()

        while len(vgScrapingEntities) > 0:
            time.sleep(3)
            print "Active threads:", threading.active_count(), \
                "Queue length:", len(vgScrapingEntities), \
                "currentThread:", threading.current_thread, \
                "In Progress:", vgEntitiesInProgress

            # for th in threading.enumerate():
            #     print(th)
            #     traceback.print_stack(sys._current_frames()[th.ident])
            #     print()

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

    def getSIID(self, scrapingItem):
        raise Exception(
            "method getSIID must be implemented in a runner class")
