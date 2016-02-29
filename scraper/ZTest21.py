# -*- coding: utf-8 -*-
from scraper.scraperPurchase import DBSaver, ScrapZakupkiGovRu

dbSaver = DBSaver()
scraper = ScrapZakupkiGovRu()
scraper.initializeWebdriver(useProxy=False)

scrapingItem = dbSaver.getPurchase(39075)
scraper.scrapOrderContent(dbSaver, scrapingItem)