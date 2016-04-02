# -*- coding: utf-8 -*-

##############################################################################################################
### run searches by keywords and save links to purchase orders
##############################################################################################################



from WorkerThread import *
from ScrapingTask import *
import urllib


class WDFnewPurchases(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        # raise Exception("method getScrapingEntitiesFromDBS must be implemented in a runner class")
        return dbSaver.getQueryStrings()

    def runScrapingForEntity(self, dbSaver, scraper, scrapingItem):
        # raise Exception("method runScrapingForEntity must be implemented in a runner class")
        # for example:
        # scraper.scrapOrderContent(dbSaver, scrapingItem)
        # dbSaver.touchPurchase(scrapingItem.purchaseId)
        scr = 'http://zakupki.gov.ru/epz/order/quicksearch/update.html?placeOfSearch=FZ_44&_placeOfSearch=on&placeOfSearch=FZ_223&_placeOfSearch=on&_placeOfSearch=on&priceFrom=0&priceTo=200+000+000+000&publishDateFrom=&publishDateTo=&updateDateFrom=&updateDateTo=&orderStages=AF&_orderStages=on&orderStages=CA&_orderStages=on&orderStages=PC&_orderStages=on&orderStages=PA&_orderStages=on&sortDirection=false&sortBy=UPDATE_DATE&recordsPerPage=_50&pageNo=1&strictEqual=false&morphology=false&showLotsInfo=false&isPaging=false&isHeaderClick=&checkIds='
        # &searchString=%D0%90%D0%BA%D0%B0%D0%B4%D0%B5%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9+%D0%A0%D0%B0%D0%B9%D0%BE%D0%BD+%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%8B
        scr += '&searchString=' + urllib.quote(scrapingItem[1])
        scraper.scrapHeaders(dbSaver, scrapingItem[0], scr)
        dbSaver.touchQuery(scrapingItem[0])
        print "####### DONE FOR Search ", urllib.quote(scrapingItem[0]), " by ", threading.current_thread(), time.time()

    def getSIID(self, scrapingItem):
        return "purch" + str(scrapingItem[0])

    def useProxy(self):
        return False


if __name__ == "__main__":
    df = WDFnewPurchases()
    WorkerThread.startScrapingEngine(df, threadsCount=3)
