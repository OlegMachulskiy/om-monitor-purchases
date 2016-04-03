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

from PurchasesPostETL import *


class PageParserPurchaseRequest:
    def __init__(self, dbSaver, driver):
        self.dbSaver = dbSaver
        self.driver = driver

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

        purchaseId = vPurchase.purchaseId
        contractTableAs = self.driver.find_elements_by_xpath('//table[@id="contract"]//a[contains(@onclick, "223/contract/public/contract/view/general-information.html?id=")]')
        ### list can be empty. Do not put driver-wait here
        for ctA in contractTableAs:
            url = ctA.get_attribute('onclick')
            url = url[len("window.open('"):-len("'); return false;")]
            # contractNo = cttds[0].text
            # customerName = cttds[1].text
            # winnerName = cttds[2].text
            # priceT = cttds[3].text
            # pushishDateT = cttds[4].text
            vPurchase.purchaseContract = PurchaseContract(purchaseId, url)
            # print "PurchaseContract:", pcontr
            self.dbSaver.storePurchaseContract(vPurchase.purchaseContract)

    def readTabProtocols(self, vPurchase):
        protocolLikeLinks = self.driver.find_elements_by_xpath(
            '//table[@class="protocolsTable"]//tr/td//a[contains(@onclick, "purchase/protocol/pz_ep/view-protocol.")]')
        for prA in protocolLikeLinks:
            url = prA.get_attribute('onclick')
            url = "http://zakupki.gov.ru" + url[len("window.open('"):-len("'); return false;")]
            prot = PurchaseProtocol(purchaseId=vPurchase.purchaseId, protocol_url=url)
            self.dbSaver.storePurchaseProtocol(prot)

        # for href in protocolLikeLinks:
        #     if u"protocolInfoId=" in href.get_attribute("onclick"):
        #         ### FOUND ON THIS SERVER. Other Servers will have different URLs
        #         href.click()
        #         self.parseBidList_ZakupkiGovRu(vPurchase)
        #         break
        #     elif u"etp-micex.ru/procedure/protocol" in href.get_attribute("href"):
        #         self.driver.get(href.get_attribute("href"))
        #         # href.click()
        #         self.parseBidList_EtpMicex(vPurchase)
        #         break
        pass

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
            PurchasesPostETL(self.dbSaver.conn).runPostETL_for_Purchase(vPurchase)
        else:
            msg = "Error: empty data map for purchase:"
            ex = Exception(msg + str(vPurchase))
            self.dbSaver.logErr(msg, ex)
            raise ex

        resultsTab = self.driver.find_elements_by_xpath('//table[@class="contentTabsWrapper"]//td/span[text()="Сведения о договоре"]')
        try:
            if len(resultsTab) > 0:
                resultsTab[0].click()
                self.readTabSupplierResults(vPurchase)
            else:
                pass  ### no results tab present on the page
        except Exception as ex:
            traceback.print_exc()
            self.dbSaver.logErr("Warning: cannot read  SUPPLIER_RESULTS tab:" + vPurchase._url, sys.exc_info())

        protoclTab = self.driver.find_elements_by_xpath('//table[@class="contentTabsWrapper"]//td/span[text()="Протоколы"]')
        try:
            if len(protoclTab) > 0:
                protoclTab[0].click()
                self.readTabProtocols(vPurchase)
            else:
                pass  ### no protocol tab on the page
        except Exception as ex:
            traceback.print_exc()
            self.dbSaver.logErr("Warning: cannot read PROTOCOLS tab:" + vPurchase._url, sys.exc_info())


if __name__ == '__main__':
    # scraper = ScrapZakupkiGovRu()
    # scraper
    dbSaver = DBSaver()
    wdm = WebDrvManager(useFirefoxDriver=True)

    ppr = PageParserPurchaseRequest(dbSaver, wdm.driver)
    prcs = dbSaver.getPurchases(purchaseId=1049)
    ppr.scrapOrderContent(prcs[0])
# ActionChains(self.driver).key_down(Keys.CONTROL).click(ctA).key_up(Keys.CONTROL).perform()
# ctA.send_keys(Keys.CONTROL + Keys.RETURN)
# self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
# self.driver.switch_to_window(main_window)
# self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
# self.driver.switch_to_window(main_window)
