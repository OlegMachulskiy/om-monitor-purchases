import re

from selenium import webdriver
from WebDrvManager import WebDrvManager

from Purchase import *
from PageParserPurchaseRequest import *
from PageParserContract import *
from OrganizationFinder import *

from PageParserPurchaseBid import *
import platform


class ScrapZakupkiGovRu(WebDrvManager):
    def __init__(self):
        pass

    def __del__(self):
        self.WebDrvManager.__del__()

    def truncOrderId(self, orderId):
        m = re.search("\d", orderId)
        if m:
            return orderId[m.start():]
            # print "Digit found at position %d" % m.start()
        else:
            return orderId
            # print "No digit in that string"

    def scrapHeaders(self, dbSaver, queryId, scrapingUrl):
        self.dbSaver = dbSaver
        print "Start scraping: ", queryId, threading.current_thread()

        self.driver.get(scrapingUrl)

        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="registerBox"]/table/tbody')))

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
                print '  Jump next page', queryId, threading.current_thread()
                nextLinks[0].click()
                element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="registerBox"]/table/tbody')))
            else:
                vContinue = False

    def scrapOrderContent(self, dbSaver, vPurchase):
        ppr = PageParserPurchaseRequest(dbSaver, self.driver)
        ppr.scrapOrderContent(vPurchase)

    def scrapPurchaseContract(self, dbSaver, purchContr):
        ppr = PageParserContract(dbSaver, self.driver)
        ppr.scrapContract(purchContr)

    def lookupOrganizationInfo(self, dbSaver, vOrg):
        orgf = OrganizationFinder(dbSaver, self.driver)
        orgf.lookupOrganizationInfo(vOrg)

    def scrapPurchaseBid(self, dbSaver, vBid):
        ppb = PageParserPurchaseBid(dbSaver, self.driver)
        ppb.scrapPurchaseBid(vBid)
