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
        print "####### DONE FOR ", scrapingItem, " by ", threading.current_thread()

    def getSIID(self, scrapingItem):
        return str(scrapingItem.purchaseContractId)


PurchasesPostETL(DBSaver().conn).runQueriesList0(PurchasesPostETL.sqls1)

df = WorkerDataFacadePR()
WorkerThread.startScrapingEngine(df, threadsCount=10)



