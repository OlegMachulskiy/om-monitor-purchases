# -*- coding: utf-8 -*-
from scraper.scraperPurchase import DBSaver, ScrapZakupkiGovRu
import json

#########################################################################################################################################################################################################
## "Manually" scrap purchase with specified ID
#########################################################################################################################################################################################################

import re

class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

dbSaver = DBSaver()
purchases = dbSaver.getPurchases()
for p in purchases:
    print p.to_JSON()
