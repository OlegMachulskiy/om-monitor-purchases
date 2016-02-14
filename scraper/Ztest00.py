from scraperPurchase import *

dbs = DBSaver()

paths = [
    "http://zakupki.gov.ru/epz/order/quicksearch/search.html?searchString=%D0%A3%D0%BF%D1%80%D0%B0%D0%B2%D0%B0+%D0%B3%D0%B0%D0%B3%D0%B0%D1%80%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%D0%B0",
    "http://zakupki.gov.ru/epz/order/quicksearch/search.html?searchString=%D0%96%D0%B8%D0%BB%D0%B8%D1%89%D0%BD%D0%B8%D0%BA+%D0%B3%D0%B0%D0%B3%D0%B0%D1%80%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%D0%B0",
    """http://zakupki.gov.ru/epz/order/quicksearch/update.html?placeOfSearch=FZ_44&_placeOfSearch=on&placeOfSearch=FZ_223&_placeOfSearch=on&_placeOfSearch=on&priceFrom=0&priceTo=200+000+000+000&publishDateFrom=&publishDateTo=&updateDateFrom=&updateDateTo=&orderStages=AF&_orderStages=on&orderStages=CA&_orderStages=on&_orderStages=on&_orderStages=on&sortDirection=false&sortBy=UPDATE_DATE&recordsPerPage=_10&pageNo=1&searchString=%D0%9B%D0%B5%D0%BD%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D0%BF%D1%80%D0%BE%D1%81%D0%BF%D0%B5%D0%BA%D1%82&strictEqual=false&morphology=false&showLotsInfo=false&isPaging=false&isHeaderClick=&checkIds=""",
    "http://zakupki.gov.ru/epz/order/quicksearch/update.html?placeOfSearch=FZ_44&_placeOfSearch=on&placeOfSearch=FZ_223&_placeOfSearch=on&_placeOfSearch=on&priceFrom=0&priceTo=200+000+000+000&publishDateFrom=&publishDateTo=&updateDateFrom=&updateDateTo=&orderStages=AF&_orderStages=on&orderStages=CA&_orderStages=on&_orderStages=on&_orderStages=on&sortDirection=false&sortBy=UPDATE_DATE&recordsPerPage=_10&pageNo=1&searchString=%D0%A3%D0%BD%D0%B8%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%82%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D0%B9+%D0%BF%D1%80%D0%BE%D1%81%D0%BF%D0%B5%D0%BA%D1%82&strictEqual=false&morphology=false&showLotsInfo=false&isPaging=false&isHeaderClick=&checkIds="
]

for p in paths:
    scraper = ScrapZakupkiGovRu(p)
    scraper.scrap(dbs)
