# -*- coding: utf-8 -*-

##############################################################################################################
### run searches by keywords and save links to purchase orders
##############################################################################################################

import random
import urllib
import threading

from scraperPurchase import *

import random
import urllib
import threading

from scraperPurchase import *
import random
import threading
import urllib
import time

from scraperPurchase import *

thread_lock = threading.Lock()

vgScrapingEntities = None
vgDBS = DBSaver()

class WorkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        WorkerThread.loadScrapingEntities()

    @staticmethod
    def loadScrapingEntities():
        global vgScrapingEntities
        global vgDBS
        if vgScrapingEntities == None or len(vgScrapingEntities) < threading.active_count():
            with thread_lock:
                vgScrapingEntities = vgDBS.getQueryStrings()
                print "vgScrapingEntities: ", len(vgScrapingEntities), ":", vgScrapingEntities[:32]

    @staticmethod
    def getScrapingEntity():
        global vgScrapingEntities
        with thread_lock:
            theObj = None
            if len(vgScrapingEntities) > 0:
                idx = random.randint(0, len(vgScrapingEntities) - 1)
                theObj = vgScrapingEntities[idx]
                vgScrapingEntities.pop(idx)
            if len(vgScrapingEntities) % 10 == 0:
                print "####Left in queue:", len(vgScrapingEntities), "threads:", threading.active_count()
            return theObj

    def run(self):
        try:
            self.scraper = ScrapZakupkiGovRu('http://www.ya.ru')
            self.scraper.initializeWebdriver(useProxy=True)
            self.dbSaver = DBSaver()

            doRun = True
            while doRun:
                scrapingItem = WorkerThread.getScrapingEntity()
                if scrapingItem == None:
                    doRun = False
                else:
                    scr = 'http://zakupki.gov.ru/epz/order/quicksearch/update.html?placeOfSearch=FZ_44&_placeOfSearch=on&placeOfSearch=FZ_223&_placeOfSearch=on&_placeOfSearch=on&priceFrom=0&priceTo=200+000+000+000&publishDateFrom=&publishDateTo=&updateDateFrom=&updateDateTo=&orderStages=AF&_orderStages=on&orderStages=CA&_orderStages=on&orderStages=PC&_orderStages=on&orderStages=PA&_orderStages=on&sortDirection=false&sortBy=UPDATE_DATE&recordsPerPage=_50&pageNo=1&strictEqual=false&morphology=false&showLotsInfo=false&isPaging=false&isHeaderClick=&checkIds='
                    # &searchString=%D0%90%D0%BA%D0%B0%D0%B4%D0%B5%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9+%D0%A0%D0%B0%D0%B9%D0%BE%D0%BD+%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%8B
                    scr += '&searchString=' + urllib.quote(scrapingItem[1])
                    self.scraper.scrapHeaders(self.dbSaver, scrapingItem[0], scr)
                    self.dbSaver.touchQuery(scrapingItem[0])

        finally:
            pass


# PurchasesPostETL(vgDBS.conn).runQueriesList0(PurchasesPostETL.sqls1)

threads = []
threads.append(WorkerThread())

for i in range(0, len(threads)):
    threads[i].start()

while len(vgScrapingEntities) > 0:
    time.sleep(3)
    print "Active threads:", threading.active_count()
    if threading.active_count() < 10:
        with(thread_lock):
            wts = WorkerThread()
            threads.append(wts)
            wts.start()

for t in threading.enumerate():
    if t != threading.current_thread():
        t.join()
