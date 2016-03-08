# -*- coding: utf-8 -*-
from scraper.scraperPurchase import DBSaver, ScrapZakupkiGovRu

dbSaver = DBSaver()
scraper = ScrapZakupkiGovRu()
scraper.initializeWebdriver(useProxy=False, useFirefoxDriver=True)

for i in [39611,31308,7292,7198,29391,110]:
    scrapingItem = dbSaver.getPurchase(i)
    scraper.scrapOrderContent(dbSaver, scrapingItem)


