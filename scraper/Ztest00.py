import random
import urllib

from scraperPurchase import *



dbs = DBSaver()
queries = dbs.getQueryStrings()
print queries

for key, value in queries.iteritems():
    scr = 'http://zakupki.gov.ru/epz/order/quicksearch/update.html?placeOfSearch=FZ_44&_placeOfSearch=on&placeOfSearch=FZ_223&_placeOfSearch=on&_placeOfSearch=on&priceFrom=0&priceTo=200+000+000+000&publishDateFrom=&publishDateTo=&updateDateFrom=&updateDateTo=&orderStages=AF&_orderStages=on&orderStages=CA&_orderStages=on&orderStages=PC&_orderStages=on&orderStages=PA&_orderStages=on&sortDirection=false&sortBy=UPDATE_DATE&recordsPerPage=_10&pageNo=1&strictEqual=false&morphology=false&showLotsInfo=false&isPaging=false&isHeaderClick=&checkIds='
    # &searchString=%D0%90%D0%BA%D0%B0%D0%B4%D0%B5%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9+%D0%A0%D0%B0%D0%B9%D0%BE%D0%BD+%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%8B
    scr += '&searchString=' + urllib.quote(value)
    scraper = ScrapZakupkiGovRu(scr)
    scraper.scrapHeaders(dbs, key)
    dbs.touchQuery(key)