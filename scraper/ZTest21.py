# -*- coding: utf-8 -*-

##############################################################################################################
### TEST NEW CODE: read existing list of purchase orders and load details
##############################################################################################################

from WorkerThread import *


class WorkerDataFacadePR(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        # raise Exception("method getScrapingEntitiesFromDBS must be implemented in a runner class")
        return dbSaver.getPurchases(1)

    def runScrapingForEntity(self, dbSaver, scraper, scrapingItem):
        # raise Exception("method runScrapingForEntity must be implemented in a runner class")
        # for example:
        scraper.scrapOrderContent(dbSaver, scrapingItem)
        dbSaver.touchPurchase(scrapingItem.purchaseId)


df = WorkerDataFacadePR()
WorkerThread.startScrapingEngine(df)
