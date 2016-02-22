import random
import urllib

from scraperPurchase import *

dbs = DBSaver()

depths = [0, 1]
for dep in depths:
    purchContracts = dbs.getPurchaseContracts(dep)
    print purchContracts[:100]

    scraper = ScrapZakupkiGovRu('http://www.ya.ru')
    scraper.initializeWebdriver()

    while len(purchContracts) > 0:
        idx = random.randint(0, len(purchContracts) - 1)
        purchContr = purchContracts[idx]
        purchContracts.pop(idx)

        scraper.scrapPurchaseContract(dbs, purchContr)
        dbs.touchPurchaseContract(purchContr.purchaseContractId)

        if len(purchContracts) % 10 == 0:
            print "Left in queue:", len(purchContracts), " for ", dep
