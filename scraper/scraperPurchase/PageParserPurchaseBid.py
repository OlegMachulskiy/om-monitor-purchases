# -*- coding: utf-8 -*-
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0

from Purchase import *


class PageParserPurchaseBid:
    def __init__(self, dbSaver, driver):
        self.dbSaver = dbSaver
        self.driver = driver

    def readTabBidData(self):
        # fullTextHTML = self.driver.page_source
        # open("file02.html", "w").write(fullTextHTML.encode('utf-8'))
        d = {}
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="noticeTabBoxWrapper"]')))

        dataTRs = self.driver.find_elements_by_xpath(
            '//div[@class="noticeTabBoxWrapper"]/table/tbody/tr')
        # if len(dataTRs) < 1:
        #     raise Exception("Page returned by proxy has no data:", self.driver.current_url)

        for dtr in dataTRs:
            tds = dtr.find_elements_by_xpath("td")
            if len(tds) > 1:
                vKey = tds[0].text
                vValue = tds[1].text
                d[vKey] = vValue

        # dataTRs = self.driver.find_elements_by_xpath(
        #     '//table[@class="participantInfoTable"]/tbody/tr')
        # for dtr in dataTRs:
        #     tds = dtr.find_elements_by_xpath("td")
        #     if len(tds) > 1:
        #         vKey = tds[0].text
        #         vValue = tds[1].text
        #         d["participantInfoTable:" + vKey] = vValue

        return d

    def scrapPurchaseBid(self, vBid):
        self.driver.get(vBid.url)
        bidRawData = self.readTabBidData()
        self.dbSaver.storePurchaseBidRawData(vBid.bidId, bidRawData)
        self.dbSaver.updatePurchaseBidData(vBid.bidId)
        pass
