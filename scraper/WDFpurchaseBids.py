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
from ScrapingTask import *

class WDFpurchaseBids(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        return dbSaver.getPurchaseBids()

    def runScrapingForEntity(self, dbSaver, scraper, scrapingItem):
        scraper.scrapPurchaseBid(dbSaver, scrapingItem)
        print "####### DONE FOR BID ", scrapingItem.bidId, " by ", threading.current_thread(), time.time()

    def getSIID(self, scrapingItem):
        return "bid" + str(scrapingItem.bidId)

    # def defaultHttpTimeout(self):
    #     return 60
    def collectProxyStats(self):
        return True


if __name__ == "__main__":
    PurchasesPostETL(DBSaver().conn).runQueriesList0(PurchasesPostETL.sqls1)
    df = WDFpurchaseBids()
    WorkerThread.startScrapingEngine(df, threadsCount=8)
