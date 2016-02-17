import random
import urllib

from scraperPurchase import *



dbs = DBSaver()
purchases = dbs.getPurchases()
print purchases

scraper = ScrapZakupkiGovRu('http://www.yandex.ru')
scraper.initializeWebdriver()

while len(purchases)>0:
    idx = random.randint(0, len(purchases) - 1)
    purchase = purchases[idx]
    purchases.pop(idx)

    scraper.scrapOrderContent(dbs, purchase)
    dbs.touchPurchase(purchase.purchaseId)

    if len(purchases)%10==0:
        print "Left in queue:", len(purchases)