# -*- coding: utf-8 -*-
from scraper.scraperPurchase import DBSaver, ScrapZakupkiGovRu

#########################################################################################################################################################################################################
## "Manually" scrap purchase with specified ID
#########################################################################################################################################################################################################

import re

dbSaver = DBSaver()
scraper = ScrapZakupkiGovRu()
scraper.initializeWebdriver(useProxy=False, useFirefoxDriver=True)

for i in [38840]:
    scrapingItem = dbSaver.getPurchase(i)
    scraper.scrapOrderContent(dbSaver, scrapingItem)


# orgText = u'Общество с ограниченной ответственностью "МинералОпт" (ИНН 5905291122)'
# match = re.search(ur'\(ИНН\s+(\d+)\)', orgText)
# print match
#
# v = match.group(0)
# print v
# print v[5:-1].strip()
# print v[4:-1].strip()
