# -*- coding: utf-8 -*-

##############################################################################################################
### read existing list of purchase orders and load details
##############################################################################################################


import threading

from PageParserPurchaseRequest import *
from WebDrvManager import *
from AbstractWorkerDataFacade import *



class WDFpurchaseDetails(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        # raise Exception("method getScrapingEntitiesFromDBS must be implemented in a runner class")
        rv = dbSaver.getPurchases(0)
        if len(rv) == 0:
            rv = dbSaver.getPurchases(1)
        return rv

    def runScrapingForEntity(self, dbSaver, webDriverM, scrapingItem):
        # raise Exception("method runScrapingForEntity must be implemented in a runner class")
        # for example:
        ppr = PageParserPurchaseRequest(dbSaver, webDriverM.driver)
        ppr.scrapOrderContent(scrapingItem)

        dbSaver.touchPurchase(scrapingItem.purchaseId)
        print "####### DONE FOR P_Details ", scrapingItem, " by ", threading.current_thread(), time.time()

    def getSIID(self, scrapingItem):
        return "pdet" + str(scrapingItem.purchaseId)

    def collectProxyStats(self):
        return True


if __name__ == "__main__":
    df = WDFpurchaseDetails()
    dbSaver = DBSaver()
    wdm = WebDrvManager(useFirefoxDriver=True)
    queue = df.getScrapingEntitiesFromDBS(dbSaver)
    for item in queue:
        df.runScrapingForEntity(dbSaver, wdm, item)
