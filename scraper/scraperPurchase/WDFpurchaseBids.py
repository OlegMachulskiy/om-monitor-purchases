# -*- coding: utf-8 -*-

##############################################################################################################
### read details for PurchaseBids  from zakupki.gov.ru
##############################################################################################################


import threading

from DBSaver import *
from PageParserPurchaseBid import *
from scraper.scraperPurchase import *
from scraper.scraperPurchase.AbstractWorkerDataFacade import *


class WDFpurchaseBids(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        return dbSaver.getPurchaseBids()

    def runScrapingForEntity(self, dbSaver, webDriverM, scrapingItem):
        ppb = PageParserPurchaseBid(dbSaver, webDriverM.driver)
        ppb.scrapPurchaseBid(scrapingItem)
        print "####### DONE FOR BID ", scrapingItem.bidId, " by ", threading.current_thread(), time.time()

    def getSIID(self, scrapingItem):
        return "bid" + str(scrapingItem.bidId)

    # def defaultHttpTimeout(self):
    #     return 60
    def collectProxyStats(self):
        return True


if __name__ == "__main__":
    df = WDFpurchaseContracts()
    dbSaver = DBSaver()
    wdm = WDFpurchaseBids(useFirefoxDriver=True)
    queue = df.getScrapingEntitiesFromDBS(dbSaver)
    for item in queue:
        df.runScrapingForEntity(dbSaver, wdm, item)
