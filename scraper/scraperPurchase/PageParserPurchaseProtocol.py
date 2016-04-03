# -*- coding: utf-8 -*-


import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0

from Purchase import *
from enum import Enum
import re
from DBSaver import DBSaver
from WebDrvManager import WebDrvManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import traceback


class PageParserPurchaseProtocol:
    def parseBidList_ZakupkiGovRu(self, vPurchase):
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//td[@tab="PROTOCOL_BID_LIST" or @tab="PROTOCOL_BID_LOT_LIST"]')))

            element.click()

            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//table[@id="protocolBid"]/tbody/tr/td[@class="firstTd" or @class="center descriptTenderTd"]//a')))

            bids = self.driver.find_elements_by_xpath('//table[@id="protocolBid"]/tbody/tr')
            for bidRow in bids:
                bidAs = bidRow.find_elements_by_xpath('td[@class="firstTd"]//a')
                if len(bidAs) > 0:
                    bidUrl = bidAs[0].get_attribute("href")
                    self.dbSaver.storePurchaseBid(vPurchase.purchaseId, bidUrl)
                else:  ## new design
                    orgName = bidRow.find_elements_by_xpath("td[3]")[0].text
                    noticeSign = bidRow.find_elements_by_xpath('td//span[@class="noticeSign"]')[0]
                    noticeSign.click()
                    noticeSignAs = noticeSign.find_elements_by_xpath('.//a')
                    bidHref = noticeSignAs[0].get_attribute("href")
                    self.dbSaver.storePurchaseBid(purchaseId=vPurchase.purchaseId, bidUrl=bidHref, participantName=orgName)


        except Exception as ex:
            eMsg = "There's no PROTOCOL_BID_LIST link here:"
            self.dbSaver.logErr(eMsg + self.driver.current_url, sys.exc_info())
            # filesList = self.readPurchaseFiles(vPurchase.purchaseId)
            # print "filesList:", filesList
            # self.dbSaver.storePurchaseFiles(vPurchase.purchaseId, filesList)

    def parseBidList_EtpMicex(self, vPurchase):
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//table[@id="requests"]')))

            TDs = self.driver.find_elements_by_xpath(
                '//table[@id="requests"]/tbody/tr/td[@class="accreditationInfoFieldset"]')
            for td in TDs:
                orgText = td.text
                match = re.search(ur'\(ИНН\s+(\d+)\)', orgText)
                inn = match.group(0)[4:-1].strip()
                hrefA = td.find_element_by_xpath(".//span/a")
                bidUrl = hrefA.get_attribute("href")
                self.dbSaver.storePurchaseBid(vPurchase.purchaseId, bidUrl)

        except Exception as ex:
            eMsg = """There's no table[@id="requests"] link here:"""
            self.dbSaver.logErr(eMsg + self.driver.current_url, sys.exc_info())
