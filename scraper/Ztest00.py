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


class Purchase:
    def __init__(self):
        self.purchaseId = None
        self.orderId = None
        self.orderDate = None
        self.purchaseType = None
        self.customer_orgId = None
        self.title = None
        self.stage = None
        self.responsible = None
        self.respons_email = None
        self.respons_phone = None
        self.contractMgr = None
        self.submitStart = None
        self.submitFinish = None
        self.submitPlace = None
        self.submitConditions = None
        self.contractAmount = None
        self.contractCurrency = None
        self._url = None
        self._loadDate = None

    # def __init__(self, orderId, url):
    #     self.__init__()
    #     self.orderId = orderId;
    #     self._url = url
    def __repr__(self):
        rv = "<Purchase:";
        rv += str(self.purchaseId) + ', ';
        rv += self.orderId + ', ';
        rv += str(self._loadDate) + ', ';
        rv += self._url.encode('utf-8') + '>';
        return rv


class DBSaver:
    def __init__(self):
        self.conn = psycopg2.connect("dbname='MonitorPurchase' user='postgres' host='localhost' password='q1w2e3r4'")
        self.journalId = None

    def testDbConnecivity(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT * from tJournal""")
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            print row

    def logErr(self, msg, exc):
        (exc_type, exc_value, exc_traceback) = exc
        cur = self.conn.cursor()
        print (str(msg.encode('utf-8')), str(exc_type.encode('utf-8')), str(exc_value.encode('utf-8')),
               traceback.format_tb(exc_traceback))
        cur.execute("""insert into tErrorLog (message, exc_type, exc_value, exc_traceback) values (%s, %s, %s, %s)
                """, (
            str(msg.encode('utf-8'))[:500], str(exc_type)[:500], str(exc_value)[:500],
            traceback.format_tb(exc_traceback)))
        self.conn.commit()
        cur.close()

    def storePurchase(self, orderId, url):
        """
        returns Purchase structure for either existing or new Purchase
        """
        cur = self.conn.cursor()
        try:

            cur.execute(
                """select purchaseId, orderId, _url, _loadDate from tPurchase where orderId=%s and _url like %s """,
                [str(orderId), str('%' + url)])
            purchases = cur.fetchall()
            loadDate = None
            purchaseId = None
            if len(purchases) == 0:
                cur.execute("""select nextval('idGen')""")
                purchaseId = cur.fetchone()[0]
                cur.execute("""insert into tPurchase (purchaseId, orderId, _url) values
                (%s,%s,%s) """, (purchaseId, orderId[:35], url))
                print "created Purchase:", purchaseId, orderId, url
                self.conn.commit()
            else:
                purchaseId = purchases[0][0]
                loadDate = purchases[0][3]
                print "Purchase exists:", purchaseId, orderId, url, loadDate
            p = Purchase()
            p.purchaseId = purchaseId
            p.orderId = orderId
            p._loadDate = loadDate
            p._url = url
            return p
        except:
            traceback.print_tb(sys.exc_traceback)
            self.logErr("No Purchase: " + orderId, sys.exc_info())
            raise NameError("No Purchase: " + orderId)
        finally:
            cur.close()


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
            print("Created webDriver for: " + self.scrapingUrl)

    def __del__(self):
        if self.driver != None:
            self.driver.quit()

    def scrap(self, dbSaver):
        self.dbSaver = dbSaver
        print "Start scraping: ", self.scrapingUrl
        self.initializeWebdriver()

        vContinue = True

        while vContinue:
            tenderTDs = self.driver.find_elements_by_xpath(
                '//div[@class="registerBox"]/table/tbody/tr/td[@class="descriptTenderTd"]')
            for ttd in tenderTDs:
                orderA = ttd.find_element_by_xpath('dl/dt/a')
                vUrl = orderA.get_attribute('href')
                orderId = orderA.text.encode('utf-8')

                vPurchase = self.dbSaver.storePurchase(orderId, vUrl)
                if vPurchase == None:
                    print "Not in DB:", vUrl, orderId
                else:
                    print "Found in DB:", vPurchase

            nextLinks = self.driver.find_elements_by_xpath('//ul[@class="paging"]/li[@class="rightArrow"]/a')
            if len(nextLinks)>0:
                nextLinks[0].click()
            else:
                vContinue = False


dbs = DBSaver()

scraper = ScrapZakupkiGovRu(
    "http://zakupki.gov.ru/epz/order/quicksearch/search.html?searchString=%D0%B3%D0%B0%D0%B3%D0%B0%D1%80%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%D0%B0")
scraper.scrap(dbs)
