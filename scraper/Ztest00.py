from scraperPurchase import *


dbs = DBSaver()

scraper = ScrapZakupkiGovRu(
    "http://zakupki.gov.ru/epz/order/quicksearch/search.html?searchString=%D0%A3%D0%BF%D1%80%D0%B0%D0%B2%D0%B0+%D0%B3%D0%B0%D0%B3%D0%B0%D1%80%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%D0%B0")
scraper.scrap(dbs)
