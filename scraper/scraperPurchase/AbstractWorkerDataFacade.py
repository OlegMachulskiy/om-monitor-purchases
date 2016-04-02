# -*- coding: utf-8 -*-

class AbstractWorkerDataFacade:
    def getScrapingEntitiesFromDBS(self, dbSaver):
        raise Exception(
            "method getScrapingEntitiesFromDBS must be implemented in a runner class")
        # for example return dbs.getPurchases(1)

    def runScrapingForEntity(self, dbSaver, webDriverM, scrapingItem):
        raise Exception(
            "method runScrapingForEntity must be implemented in a runner class")
        # for example:
        # self.scraper.scrapOrderContent(self.dbSaver, scrapingItem)
        # self.dbSaver.touchPurchase(scrapingItem.purchaseId)

    def getSIID(self, scrapingItem):
        raise Exception(
            "method getSIID must be implemented in a runner class")

    def collectProxyStats(self):
        return False

    def defaultHttpTimeout(self):
        return 50

    def useProxy(self):
        return True
