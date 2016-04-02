# -*- coding: utf-8 -*-
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0

from Purchase import *
from DBSaver import DBSaver
from WebDrvManager import WebDrvManager

import re


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
        if vBid.participantName is None:
            self.driver.get(vBid.url)
            bidRawData = self.readTabBidData()
            self.dbSaver.storePurchaseBidRawData(vBid.bidId, bidRawData)
            self.dbSaver.updatePurchaseBidData(vBid.bidId)
        else:  ## name is present!!!! lookup INN!
            self.driver.get('http://www.list-org.com/?search=name')
            searchFld = self.driver.find_elements_by_xpath('//input[@name="val"]')[0]
            pName = vBid.participantName.decode('utf-8')
            searchFld.send_keys(pName)
            searchFld.find_element_by_xpath('../button').click()
            vPs = self.driver.find_elements_by_xpath('//div[@class="content"]/p/a')
            vPs[0].click()
            vPs = self.driver.find_elements_by_xpath('//div[@class="content"]/p/i[text()="ИНН:"]/..')
            tINN = vPs[0].text
            inn_ = tINN[5:]
            dbSaver.storePurchaseBidRawData(vBid.bidId, {u'ИНН' : inn_})
            self.dbSaver.updatePurchaseBidData(vBid.bidId)

        pass


if __name__ == '__main__':
    # scraper = ScrapZakupkiGovRu()
    # scraper
    try:
        dbSaver = DBSaver()
        wdm = WebDrvManager(useFirefoxDriver=True)


        ppr = PageParserPurchaseBid(dbSaver, wdm.driver)
        prcs = dbSaver.getPurchaseBids(bidId=186890)
        ppr.scrapPurchaseBid(prcs[0])
    except Exception as ex:
        pass
