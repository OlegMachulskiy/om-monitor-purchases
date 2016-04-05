# -*- coding: utf-8 -*-

##############################################################################################################
### update contracts details
##############################################################################################################

import threading

from PageParserContract import *
from WebDrvManager import *
from AbstractWorkerDataFacade import *


class WDFpurchaseContracts(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        # raise Exception("method getScrapingEntitiesFromDBS must be implemented in a runner class")
        rv = dbSaver.getPurchaseContracts(0)
        if rv is None or len(rv) == 0:
            rv = dbSaver.getPurchaseContracts(1)
        return rv

    #

    def runScrapingForEntity(self, dbSaver, webDriverM, scrapingItem):

        ppr = PageParserContract(dbSaver, webDriverM.driver)
        ppr.scrapContract(scrapingItem)
        dbSaver.touchPurchaseContract(scrapingItem.purchaseContractId)
        print "####### DONE FOR PCONTR ", scrapingItem, " by ", threading.current_thread(), ' at ', datetime.datetime.now()

    def getSIID(self, scrapingItem):
        return "pcontr" + str(scrapingItem.purchaseContractId)

    def collectProxyStats(self):
        return True


if __name__ == "__main__":
    df = WDFpurchaseContracts()
    dbSaver = DBSaver()
    queue = df.getScrapingEntitiesFromDBS(dbSaver)
    for item in queue:
        wdm = WebDrvManager(useFirefoxDriver=True)

        df.runScrapingForEntity(dbSaver, wdm, item)

        del wdm
