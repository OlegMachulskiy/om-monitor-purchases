# -*- coding: utf-8 -*-

##############################################################################################################
### read organizations details from SBIS website
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


class WorkerDataFacadePR(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        # raise Exception("method getScrapingEntitiesFromDBS must be implemented in a runner class")
        return dbSaver.getOrganizations(" (p_name IS NULL AND inn IS NOT NULL)")

    def runScrapingForEntity(self, dbSaver, scraper, scrapingItem):
        # raise Exception("method runScrapingForEntity must be implemented in a runner class")
        # for example:
        # scraper.scrapOrderContent(dbSaver, scrapingItem)
        # dbSaver.touchPurchase(scrapingItem.purchaseId)
        scraper.lookupOrganizationInfo(dbSaver, scrapingItem)
        print "####### DONE FOR ", scrapingItem.partnerId, " by ", threading.current_thread()

    def getSIID(self, scrapingItem):
        return str(scrapingItem.partnerId)

    def defaultHttpTimeout(self):
        return 60


PurchasesPostETL(DBSaver().conn).runQueriesList0(PurchasesPostETL.sqls1)

df = WorkerDataFacadePR()
WorkerThread.startScrapingEngine(df, threadsCount=19)

