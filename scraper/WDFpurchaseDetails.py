# -*- coding: utf-8 -*-

##############################################################################################################
### read existing list of purchase orders and load details
##############################################################################################################


from WorkerThread import *
from ScrapingTask import *

class WDFpurchaseDetails(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        # raise Exception("method getScrapingEntitiesFromDBS must be implemented in a runner class")
        rv = dbSaver.getPurchases(0)
        if len(rv)==0:
            rv = dbSaver.getPurchases(1)
        return rv

    def runScrapingForEntity(self, dbSaver, scraper, scrapingItem):
        # raise Exception("method runScrapingForEntity must be implemented in a runner class")
        # for example:
        scraper.scrapOrderContent(dbSaver, scrapingItem)
        dbSaver.touchPurchase(scrapingItem.purchaseId)
        print "####### DONE FOR P_Details ", scrapingItem, " by ", threading.current_thread(), time.time()

    def getSIID(self, scrapingItem):
        return "pdet"+str(scrapingItem.purchaseId)

    def collectProxyStats(self):
        return True

if __name__ == "__main__":
    df = WDFpurchaseDetails()
    WorkerThread.startScrapingEngine(df, threadsCount=8)
