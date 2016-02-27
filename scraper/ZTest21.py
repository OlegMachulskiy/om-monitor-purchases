# -*- coding: utf-8 -*-

##############################################################################################################
### read existing list of purchase orders and load details
##############################################################################################################

import threading

from AbstractWorkerThread import AbstractWorkerThread
from scraperPurchase import *

thread_lock = threading.Lock()

vgScrapingEntities = None
vgDBS = DBSaver()


class WorkerLoadPR(AbstractWorkerThread):
    def getScrapingEntitiesFromDBS(self):
        raise Exception("method getScrapingEntitiesFromDBS must be implemented in a runner class")
        # for example return dbs.getPurchases(1)

    def runScrapingForEntity(self, dbSaver, scrapingItem):
        raise Exception("method runScrapingForEntity must be implemented in a runner class")
        # for example:
        # self.scraper.scrapOrderContent(self.dbSaver, scrapingItem)
        # self.dbSaver.touchPurchase(scrapingItem.purchaseId)


cl = WorkerLoadPR()
print cl
cls = globals()["WorkerLoadPR"]
print cls
inst = cls()
print inst
# AbstractWorkerThread.startScrapingEngine(WorkerLoadPR.__class__, 5)
