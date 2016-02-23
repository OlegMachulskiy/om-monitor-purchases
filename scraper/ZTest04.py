import random
import urllib
import threading

from scraperPurchase import *


scraper = ScrapZakupkiGovRu('http://www.ya.ru')
scraper.initializeWebdriver()
dbSaver = DBSaver()

purchContrs = dbSaver.getPurchaseContracts(purchaseContractId=44746)

for contr in purchContrs :
    scraper.scrapPurchaseContract(dbSaver, contr)


