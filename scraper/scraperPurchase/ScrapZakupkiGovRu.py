import datetime
from urllib2 import HTTPError

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import re

from Purchase import *


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

    def readPurchaseData(self):
        # fullTextHTML = self.driver.page_source
        # open("file02.html", "w").write(fullTextHTML.encode('utf-8'))
        dataTRs = self.driver.find_elements_by_xpath(
            '//div[@class="noticeTabBoxWrapper"]/table/tbody/tr')
        d = {}
        for dtr in dataTRs:
            tds = dtr.find_elements_by_xpath("td")
            if len(tds) > 1:
                vKey = tds[0].text
                vValue = tds[1].text
                d[vKey] = vValue
        return d

    def truncOrderId(self, orderId):
        m = re.search("\d", orderId)
        if m:
            return orderId[m.start():]
            #print "Digit found at position %d" % m.start()
        else:
            return orderId
            #print "No digit in that string"

    def readPurchaseFiles(self, purchaseId):
        # fullTextHTML = self.driver.page_source
        # open("file03.html", "w").write(fullTextHTML.encode('utf-8'))
        rv = []
        dataAs = self.driver.find_elements_by_xpath(
            '//table[@id="notice-documents"]//table//td[@style="width: 100%"]/a')
        for dA in dataAs:
            url = dA.get_attribute('href')
            title = dA.text
            filename = dA.get_attribute('title')
            if url != None and title != u'':
                pf = PurchaseFile(purchaseId, None, url, title, filename)
                rv.append(pf)
        return rv

    def scrapHeaders(self, dbSaver, queryId):
        self.dbSaver = dbSaver
        print "Start scraping: ", self.scrapingUrl
        self.initializeWebdriver()

        vContinue = True # becomes False when last page in pagination reached

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
        # do the following for purchases only once per day
        # ActionChains(self.driver).key_down(Keys.CONTROL).click(orderA).key_up(Keys.CONTROL).perform()
        # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        #
        # self.driver.switch_to_window(main_window)
        self.dbSaver = dbSaver
        self.driver.get(vPurchase._url)

        purchaseMap = self.readPurchaseData()
        # print "purchaseMap:", purchaseMap
        self.dbSaver.storePurchaseData(vPurchase.purchaseId, purchaseMap)

        purchaseTabs = self.driver.find_elements_by_xpath(
            '//table[@class="contentTabsWrapper"]//td[@tab="PURCHASE_DOCS"]')
        if len(purchaseTabs) > 0:
            purchaseTabs[0].click()
            filesList = self.readPurchaseFiles(vPurchase.purchaseId)
            print "filesList:", filesList
            self.dbSaver.storePurchaseFiles(vPurchase.purchaseId, filesList)
        else:
            print "There's no documents tab here"

        # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
        # self.driver.switch_to_window(main_window)
        # else:
        #     print "Object refreshed less than 1 day ago:", vPurchase
        #     print datetime.datetime.now(), vPurchase._loadDate, (datetime.datetime.now() - vPurchase._loadDate)
