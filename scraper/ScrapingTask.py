# -*- coding: utf-8 -*-

class ScrapingTask:
    def __init__(self, taskObject, wdf):
        self.taskObject = taskObject
        self.wdf = wdf

    # def exposed_wdf(self):
    #     return self.wdf
    #
    # def exposed_taskObject(self):
    #     return self.taskObject

    def __repr__(self):
        return "<ScrapingTask" + str(self.wdf) + ", " + str(self.taskObject) + ">"


class AbstractWorkerDataFacade:
    def getScrapingEntitiesFromDBS(self, dbSaver):
        raise Exception(
            "method getScrapingEntitiesFromDBS must be implemented in a runner class")
        # for example return dbs.getPurchases(1)

    def runScrapingForEntity(self, dbSaver, scraper, scrapingItem):
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
