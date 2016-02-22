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
                self.scraper.scrapOrderContent(self.dbSaver, scrapingItem)
                self.dbSaver.touchPurchase(scrapingItem.purchaseId)


dbs = DBSaver()

depths = [1]
for dep in depths:
    purchases = dbs.getPurchases(dep)
    print purchases[:32]

    threads = []
    for i in range(0, 8):
        threads.append(WorkerThread(purchases))

    print threads

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
