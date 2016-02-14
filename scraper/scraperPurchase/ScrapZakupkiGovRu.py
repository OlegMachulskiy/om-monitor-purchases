from urllib2 import HTTPError

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

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

    def readPurchaseFiles(self):
        # fullTextHTML = self.driver.page_source
        # open("file03.html", "w").write(fullTextHTML.encode('utf-8'))
        rv = []
        dataAs = self.driver.find_elements_by_xpath(
            '//table[@id="notice-documents"]//table//td[@style="width: 100%"]')
        for dA in dataAs:
            pf = PurchaseFile(None, None, dA.get_attribute('href'), dA.text, dA.get_attribute('title'))
            rv.append(pf)
        return rv

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

                main_window = self.driver.current_window_handle

                ActionChains(self.driver).key_down(Keys.CONTROL).click(orderA).key_up(Keys.CONTROL).perform()
                self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

                self.driver.switch_to_window(main_window)

                purchaseMap = self.readPurchaseData()
                # print "purchaseMap:", purchaseMap
                self.dbSaver.storePurchaseData(vPurchase.purchaseId, purchaseMap)

                purchaseTab = self.driver.find_element_by_xpath(
                    '//table[@class="contentTabsWrapper"]//td[@tab="PURCHASE_DOCS"]')
                purchaseTab.click()
                filesMap = self.readPurchaseFiles()
                self.dbSaver.storePurchaseFiles(vPurchase.purchaseId, filesMap)

                self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                self.driver.switch_to_window(main_window)

            nextLinks = self.driver.find_elements_by_xpath('//ul[@class="paging"]/li[@class="rightArrow"]/a')
            if len(nextLinks) > 0:
                nextLinks[0].click()
            else:
                vContinue = False
