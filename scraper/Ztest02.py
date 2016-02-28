# -*- coding: utf-8 -*-

##############################################################################################################
### update contracts details
##############################################################################################################

import random
import threading
import time

from scraperPurchase import *

from WorkerThread import *
import urllib


class WorkerDataFacadePR(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        # raise Exception("method getScrapingEntitiesFromDBS must be implemented in a runner class")
        return dbSaver.getPurchaseContracts(1)

    #

    def runScrapingForEntity(self, dbSaver, scraper, scrapingItem):
        # raise Exception("method runScrapingForEntity must be implemented in a runner class")
        # for example:
        # scraper.scrapOrderContent(dbSaver, scrapingItem)
        # dbSaver.touchPurchase(scrapingItem.purchaseId)
        scraper.scrapPurchaseContract(dbSaver, scrapingItem)
        dbSaver.touchPurchaseContract(scrapingItem.purchaseContractId)


PurchasesPostETL(DBSaver().conn).runQueriesList0(PurchasesPostETL.sqls1)

df = WorkerDataFacadePR()
WorkerThread.startScrapingEngine(df)




#
# thread_lock = threading.Lock()
#
# vgScrapingEntities = None
# vgDBS = DBSaver()
#
#
# class WorkerThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         WorkerThread.loadScrapingEntities()
#
#     @staticmethod
#     def loadScrapingEntities():
#         global vgScrapingEntities
#         global vgDBS
#         if vgScrapingEntities == None or len(vgScrapingEntities) < threading.active_count():
#             with thread_lock:
#                 vgScrapingEntities = vgDBS.getPurchaseContracts(1)
#                 print "vgScrapingEntities: ", len(vgScrapingEntities), ":", vgScrapingEntities[:32]
#
#     @staticmethod
#     def getScrapingEntity():
#         global vgScrapingEntities
#         with thread_lock:
#             theObj = None
#             if len(vgScrapingEntities) > 0:
#                 idx = random.randint(0, len(vgScrapingEntities) - 1)
#                 theObj = vgScrapingEntities[idx]
#                 vgScrapingEntities.pop(idx)
#             return theObj
#
#     def run(self):
#         self.scraper = ScrapZakupkiGovRu('http://www.ya.ru')
#         self.dbSaver = DBSaver()
#         try:
#             self.scraper = ScrapZakupkiGovRu('http://www.ya.ru')
#             self.scraper.initializeWebdriver(useProxy=True)
#             self.dbSaver = DBSaver()
#
#             doRun = True
#             while doRun:
#                 scrapingItem = WorkerThread.getScrapingEntity()
#                 if scrapingItem == None:
#                     doRun = False
#                 else:
#                     self.scraper.scrapPurchaseContract(self.dbSaver, scrapingItem)
#                     self.dbSaver.touchPurchaseContract(scrapingItem.purchaseContractId)
#         finally:
#             if self.scraper != None: del self.scraper
#             if self.dbSaver != None: del self.dbSaver
#
#
# PurchasesPostETL(vgDBS.conn).runQueriesList0(PurchasesPostETL.sqls1)
#
# threads = []
# threads.append(WorkerThread())
#
# for i in range(0, len(threads)):
#     threads[i].start()
#
# while len(vgScrapingEntities) > 0:
#     time.sleep(3)
#     print "Active threads:", threading.active_count(), "Queue length:", len(
#         vgScrapingEntities), "currentThread:", threading.current_thread
#     if threading.active_count() < 10:
#         with(thread_lock):
#             wts = WorkerThread()
#             threads.append(wts)
#             wts.start()
#
# for t in threading.enumerate():
#     if t != threading.current_thread():
#         t.join()
