# -*- coding: utf-8 -*-
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0

from Purchase import *


class PageParserPurchaseRequest:
    def __init__(self, dbSaver, driver):
        self.dbSaver = dbSaver
        self.driver = driver

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

    def readTabPurchaseData(self):
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

    def readTabSupplierResults(self, vPurchase):
        contractTableTRs = self.driver.find_elements_by_xpath('//table[@id="contract"]/tbody/tr')
        for cttr in contractTableTRs:
            cttds = cttr.find_elements_by_xpath("td")
            url = cttds[0].find_elements_by_xpath('a')[1].get_attribute("href")
            purchaseId = vPurchase.purchaseId
            contractNo = cttds[0].text
            customerName = cttds[1].text
            winnerName = cttds[2].text
            priceT = cttds[3].text
            pushishDateT = cttds[4].text
            pcontr = PurchaseContract(purchaseId, url, contractNo, customerName, winnerName, priceT,
                                      pushishDateT)
            print "PurchaseContract:", pcontr
            self.dbSaver.storePurchaseContract(pcontr)

        vProtocolFound = False
        protocolLikeLinks = self.driver.find_elements_by_xpath('//table[@class="noticeCardTableInBlock"]/tbody/tr/td/a')
        for href in protocolLikeLinks:
            if u"protocolId=" in href.get_attribute(
                    "href"):  ### FOUND ON THIS SERVER. Other Servers will have different URLs
                vProtocolFound = True
                href.click()
                break

        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//td[@tab="PROTOCOL_BID_LIST" or @tab="PROTOCOL_BID_LOT_LIST"]')))

            element.click()

            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//table[@id="protocolBid"]/tbody/tr/td[@class="firstTd" or @class="center descriptTenderTd"]//a')))

            bids = self.driver.find_elements_by_xpath('//table[@id="protocolBid"]/tbody/tr/td[@class="firstTd"]//a')
            for bidA in bids:
                bidUrl = bidA.get_attribute("href")
                self.dbSaver.storePurchaseBid(vPurchase.purchaseId, bidUrl)
        except Exception as ex:
            eMsg = "There's no PROTOCOL_BID_LIST link here:"
            self.dbSaver.logErr(eMsg + self.driver.current_url, sys.exc_info())
            # filesList = self.readPurchaseFiles(vPurchase.purchaseId)
            # print "filesList:", filesList
            # self.dbSaver.storePurchaseFiles(vPurchase.purchaseId, filesList)

    def scrapOrderContent(self, vPurchase):
        # do the following for purchases only once per several days
        # ActionChains(self.driver).key_down(Keys.CONTROL).click(orderA).key_up(Keys.CONTROL).perform()
        # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        #
        # self.driver.switch_to_window(main_window)
        self.driver.get(vPurchase._url)
        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="noticeTabBoxWrapper"]')))

        purchaseMap = self.readTabPurchaseData()
        # print "purchaseMap:", purchaseMap
        if len(purchaseMap) > 0:
            self.dbSaver.storePurchaseData(vPurchase.purchaseId, purchaseMap)
        else:
            msg = "Error: empty data map for purchase:"
            ex = Exception(msg + str(vPurchase))
            self.dbSaver.logErr(msg, ex)
            raise ex

        purchaseTabs = self.driver.find_elements_by_xpath(
            '//table[@class="contentTabsWrapper"]//td[@tab="PURCHASE_DOCS"]')
        try:
            purchaseTabs[0].click()

            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//table[@id="notice-documents"]')))

            filesList = self.readPurchaseFiles(vPurchase.purchaseId)
            # print "filesList:", filesList
            self.dbSaver.storePurchaseFiles(vPurchase.purchaseId, filesList)
        except Exception as ex:
            self.dbSaver.logErr("Warning: no PURCHASE_DOCS tab:" + vPurchase._url, sys.exc_info())

        resultsTab = self.driver.find_elements_by_xpath(
            '//table[@class="contentTabsWrapper"]//td[@tab="SUPPLIER_RESULTS"]')
        try:
            resultsTab[0].click()

            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//table[@id="contract"]/tbody/tr')))

            self.readTabSupplierResults(vPurchase)
        except Exception as ex:
            self.dbSaver.logErr("Warning: no SUPPLIER_RESULTS tab:" + vPurchase._url, sys.exc_info())

            # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
            # self.driver.switch_to_window(main_window)
            # else:
            #     print "Object refreshed less than 1 day ago:", vPurchase
            #     print datetime.datetime.now(), vPurchase._loadDate, (datetime.datetime.now() - vPurchase._loadDate)
