import re
from urllib2 import HTTPError

from selenium import webdriver

from Purchase import *
from PageParserPurchaseRequest import *
from PageParserContract import *


class ScrapZakupkiGovRu:
    def __init__(self, scrapingUrl):
        self.scrapingUrl = scrapingUrl

    def initializeWebdriver(self):
        try:
            #self.driver = webdriver.Firefox()
            self.driver = webdriver.PhantomJS("C:/usr/phantomjs-2.1.1-windows/bin/phantomjs.exe")

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

    def truncOrderId(self, orderId):
        m = re.search("\d", orderId)
        if m:
            return orderId[m.start():]
            # print "Digit found at position %d" % m.start()
        else:
            return orderId
            # print "No digit in that string"

    def scrapHeaders(self, dbSaver, queryId):
        self.dbSaver = dbSaver
        print "Start scraping: ", self.scrapingUrl
        self.initializeWebdriver()

        vContinue = True  # becomes False when last page in pagination reached

        while vContinue:
            tenderTDs = self.driver.find_elements_by_xpath(
                '//div[@class="registerBox"]/table/tbody/tr/td[@class="descriptTenderTd"]')
            for ttd in tenderTDs:
                orderA = ttd.find_element_by_xpath('dl/dt/a')
                vUrl = orderA.get_attribute('href')
                orderId = self.truncOrderId(orderA.text.encode('utf-8'))
                vPurchase = self.dbSaver.storePurchase(orderId, vUrl)
                # main_window = self.driver.current_window_handle

            nextLinks = self.driver.find_elements_by_xpath('//ul[@class="paging"]/li[@class="rightArrow"]/a')
            if len(nextLinks) > 0:
                nextLinks[0].click()
            else:
                vContinue = False

    def scrapOrderContent(self, dbSaver, vPurchase):
        ppr = PageParserPurchaseRequest(dbSaver, self.driver)
        ppr.scrapOrderContent(vPurchase)

    def scrapPurchaseContract(self, dbSaver, purchContr):
        ppr = PageParserContract(dbSaver, self.driver)
        ppr.scrapContract(purchContr)
