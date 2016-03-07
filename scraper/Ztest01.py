# -*- coding: utf-8 -*-

##############################################################################################################
### read existing list of purchase orders and load details
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
        print "####### DONE FOR ", scrapingItem, " by ", threading.current_thread()

    def getSIID(self, scrapingItem):
        return str(scrapingItem.purchaseId)

    def collectProxyStats(self):
        return True

df = WorkerDataFacadePR()
WorkerThread.startScrapingEngine(df, threadsCount=22)
