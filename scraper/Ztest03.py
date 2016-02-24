# -*- coding: utf-8 -*-

##############################################################################################################
### read organizations details from SBIS website
##############################################################################################################

import random
import threading
import urllib
import time

from scraperPurchase import *

thread_lock = threading.Lock()
global running_threads_amount

class WorkerThread(threading.Thread):

    def __init__(self, organizations):
        threading.Thread.__init__(self)
        self.organizations = organizations

    def run(self):

        global running_threads_amount
        with(thread_lock):
            running_threads_amount  += 1
        try:
            self.scraper = ScrapZakupkiGovRu('http://www.ya.ru')
            self.scraper.initializeWebdriver(useProxy=True)
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
                    # dbs.touchPurchaseContract(theOrg.purchaseContractId)
        finally:
            with(thread_lock):
                running_threads_amount  -= 1

dbs = DBSaver()
PurchasesPostETL(dbs.conn).runQueriesList0(PurchasesPostETL.sqls1)

orgs = dbs.getOrganizations(" (p_name IS NULL AND inn IS NOT NULL)")
print orgs[:32]

threads = []
running_threads_amount = 0
for i in range(0, 3):

    threads.append(WorkerThread(orgs))

for i in range(0, len(threads)):
    threads[i].start()

while len(orgs) > 0:
    time.sleep(3)
    print "Active threads:", running_threads_amount, threading.active_count()
    if running_threads_amount<8:
        with(thread_lock):
            wts = WorkerThread(orgs)
            threads.append(wts)
            wts.start()

for i in range(0, len(threads)):
    threads[i].join()
