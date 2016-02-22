import random
import threading
import urllib

from scraperPurchase import *

thread_lock = threading.Lock()

class WorkerThread(threading.Thread):
    def __init__(self, organizations):
        threading.Thread.__init__(self)
        self.organizations = organizations

    def run(self):
        self.scraper = ScrapZakupkiGovRu('http://www.ya.ru')
        self.scraper.initializeWebdriver()
        self.dbSaver = DBSaver()

        doRun = True

        while doRun:
            theOrg = None
            with(thread_lock):
                if len(self.organizations) > 0:
                    idx = random.randint(0, len(self.organizations) - 1)
                    theOrg = self.organizations[idx]
                    self.organizations.pop(idx)
                else:
                    doRun = False
                if len(self.organizations) % 10 == 0:
                    print "Left in queue:", len(self.organizations), "overall"

            if self.organizations != None:
                self.scraper.lookupOrganizationInfo(self.dbSaver, theOrg)
                #dbs.touchPurchaseContract(theOrg.purchaseContractId)


dbs = DBSaver()
PurchasesPostETL(dbs.conn).runQueriesList0(PurchasesPostETL.sqls1)

orgs = dbs.getOrganizations()
print orgs[:32]

threads = []
for i in range(0, 5):
    threads.append(WorkerThread(orgs))

for i in range(0, len(threads)):
    threads[i].start()

for i in range(0, len(threads)):
    threads[i].join()
