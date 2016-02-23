import random
import threading
import urllib

from scraperPurchase import *

thread_lock = threading.Lock()


class WorkerThread(threading.Thread):
    def __init__(self, purchContracts):
        threading.Thread.__init__(self)
        self.purchContracts = purchContracts

    def run(self):
        self.scraper = ScrapZakupkiGovRu('http://www.ya.ru')
        self.scraper.initializeWebdriver()
        self.dbSaver = DBSaver()

        doRun = True

        while doRun:
            purchContr = None
            with(thread_lock):
                if len(self.purchContracts) > 0:
                    idx = random.randint(0, len(purchContracts) - 1)
                    purchContr = purchContracts[idx]
                    purchContracts.pop(idx)
                else:
                    doRun = False
                if len(purchContracts) % 10 == 0:
                    print "Left in queue:", len(purchContracts), " for ", dep

            if purchContr != None:
                self.scraper.scrapPurchaseContract(self.dbSaver, purchContr)
                dbs.touchPurchaseContract(purchContr.purchaseContractId)


dbs = DBSaver()

depths = [0, 1]
for dep in depths:
    purchContracts = dbs.getPurchaseContracts(dep)
    print purchContracts[:100]

    threads = []
    for i in range(0, 22):
        threads.append(WorkerThread(purchContracts))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
