# -*- coding: utf-8 -*-

##############################################################################################################
### run searches by keywords and save links to purchase orders
##############################################################################################################

import random
import urllib
import threading

from scraperPurchase import *

thread_lock = threading.Lock()


class WorkerThread(threading.Thread):
    def __init__(self, queryItems):
        threading.Thread.__init__(self)
        self.queryItems = queryItems

    def run(self):
        # with(thread_lock):
        self.scraper = ScrapZakupkiGovRu('http://www.ya.ru')
        self.scraper.initializeWebdriver()
        self.dbSaver = DBSaver()

        doRun = True

        while doRun:
            scrapingItem = None
            with(thread_lock):
                if len(self.queryItems) > 0:
                    idx = random.randint(0, len(self.queryItems) - 1)
                    scrapingItem = self.queryItems[idx]
                    self.queryItems.pop(idx)
                else:
                    doRun = False
                if len(self.queryItems) % 10 == 0:
                    print "Left in queue:", len(self.queryItems)

            if scrapingItem != None:
                scr = 'http://zakupki.gov.ru/epz/order/quicksearch/update.html?placeOfSearch=FZ_44&_placeOfSearch=on&placeOfSearch=FZ_223&_placeOfSearch=on&_placeOfSearch=on&priceFrom=0&priceTo=200+000+000+000&publishDateFrom=&publishDateTo=&updateDateFrom=&updateDateTo=&orderStages=AF&_orderStages=on&orderStages=CA&_orderStages=on&orderStages=PC&_orderStages=on&orderStages=PA&_orderStages=on&sortDirection=false&sortBy=UPDATE_DATE&recordsPerPage=_10&pageNo=1&strictEqual=false&morphology=false&showLotsInfo=false&isPaging=false&isHeaderClick=&checkIds='
                # &searchString=%D0%90%D0%BA%D0%B0%D0%B4%D0%B5%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9+%D0%A0%D0%B0%D0%B9%D0%BE%D0%BD+%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%8B
                scr += '&searchString=' + urllib.quote(scrapingItem[1])
                self.scraper.scrapHeaders(self.dbSaver, scrapingItem[0], scr)
                self.dbSaver.touchQuery(scrapingItem[0])


dbs = DBSaver()
queries = dbs.getQueryStrings()
print "dbs.getQueryStrings():", queries[:32]
threads = []
for i in range(0, 12):
    threads.append(WorkerThread(queries))

print "threads:", threads
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
