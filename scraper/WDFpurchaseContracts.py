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
from ScrapingTask import *

class WDFpurchaseContracts(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        # raise Exception("method getScrapingEntitiesFromDBS must be implemented in a runner class")
        rv = dbSaver.getPurchaseContracts(0)
        if rv is None or len(rv)==0:
            rv = dbSaver.getPurchaseContracts(1)
        return rv

    #

    def runScrapingForEntity(self, dbSaver, scraper, scrapingItem):
        # raise Exception("method runScrapingForEntity must be implemented in a runner class")
        # for example:
        # scraper.scrapOrderContent(dbSaver, scrapingItem)
        # dbSaver.touchPurchase(scrapingItem.purchaseId)
        scraper.scrapPurchaseContract(dbSaver, scrapingItem)
        dbSaver.touchPurchaseContract(scrapingItem.purchaseContractId)
        print "####### DONE FOR PCONTR ", scrapingItem, " by ", threading.current_thread()

    def getSIID(self, scrapingItem):
        return "pcontr" + str(scrapingItem.purchaseContractId)

    def collectProxyStats(self):
        return True


if __name__ == "__main__":
    PurchasesPostETL(DBSaver().conn).runQueriesList0(PurchasesPostETL.sqls1)

    df = WDFpurchaseContracts()
    WorkerThread.startScrapingEngine(df, threadsCount=8)
