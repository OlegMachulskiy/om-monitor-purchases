# -*- coding: utf-8 -*-

##############################################################################################################
### read details for PurchaseBids  from zakupki.gov.ru
##############################################################################################################

import random
import threading
import time

from scraperPurchase import *

import random
import threading
import time

from scraperPurchase import *

from WorkerThread import *
import urllib


class WorkerDataFacadeBids(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        return dbSaver.getPurchaseBids()

    def runScrapingForEntity(self, dbSaver, scraper, scrapingItem):
        scraper.scrapPurchaseBid(dbSaver, scrapingItem)
        print "####### DONE FOR ", scrapingItem.bidId, " by ", threading.current_thread()

    def getSIID(self, scrapingItem):
        return str(scrapingItem.bidId)

    # def defaultHttpTimeout(self):
    #     return 60
    def collectProxyStats(self):
        return True


PurchasesPostETL(DBSaver().conn).runQueriesList0(PurchasesPostETL.sqls1)

df = WorkerDataFacadeBids()
WorkerThread.startScrapingEngine(df, threadsCount=12)



