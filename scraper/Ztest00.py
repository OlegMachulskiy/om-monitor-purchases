import traceback

import webbrowser
from urllib2 import HTTPError
from urllib2 import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0

import sys
import traceback
from datetime import *

import psycopg2


class DBSaver:
    def __init__(self):
        self.conn = psycopg2.connect("dbname='MonitorZakupki' user='postgres' host='localhost' password='q1w2e3r4'")
        self.journalId = None

    def testDbConnecivity(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT * from tJournal""")
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            print row


class ScrapZakupkiGovRu:
    def __init__(self, scrapingUrl):
        self.scrapingUrl = scrapingUrl

    def initializeWebdriver(self):
        try:
            self.driver = webdriver.Firefox()
            # self.driver = webdriver.PhantomJS("C:/usr/phantomjs-2.1.1-windows/bin/phantomjs.exe")

            self.driver.get(self.scrapingUrl)
            open("file00.html", "w").write(unicode(self.driver.page_source).encode('utf-8'))
        except HTTPError as e:
            print(e)
            raise (e)
        else:
            print("Created webDriver for:" + self.scrapingUrl)

    def scrap(self, dbSaver):
        

dbs = DBSaver()

scraper = ScrapZakupkiGovRu("http://zakupki.gov.ru/epz/order/quicksearch/search.html?searchString=%D0%B3%D0%B0%D0%B3%D0%B0%D1%80%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%D0%B0")
scraper.scrap(dbs)