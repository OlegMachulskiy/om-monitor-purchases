import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
import threading
from Purchase import *
from enum import Enum
import re
from DBSaver import DBSaver
from WebDrvManager import WebDrvManager


class PageParserSearchResults:
    def __init__(self, dbSaver, driver):
        self.dbSaver = dbSaver
        self.driver = driver

    def scrapSearchResults(self, queryId, scrapingUrl):
        print "Start scraping: ", queryId, threading.current_thread()

        self.driver.get(scrapingUrl)

        xPathToWait = '//div[@class="registerBox registerBoxBank margBtm20"]/table/tbody'
        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xPathToWait)))

        # vContinue = True  # becomes False when last page in pagination reached
        previousLinkText = 'SOME FAKE TEXT'
        while True:
            tenderTDs = self.driver.find_elements_by_xpath(
                '//div[@class="registerBox registerBoxBank margBtm20"]/table/tbody/tr/td[@class="descriptTenderTd"]')
            for ttd in tenderTDs:
                orderA = ttd.find_element_by_xpath('dl/dt/a')
                vUrl = orderA.get_attribute('href')
                orderId = self.truncOrderId(orderA.text.encode('utf-8'))
                vPurchase = self.dbSaver.storePurchase(orderId, vUrl)
                # main_window = self.driver.current_window_handle

            openedPopups = self.driver.find_elements_by_xpath('//div[@class="popUpWrapper"]//input[@class="bigGreyBtn closePopUp"]')
            for popup in openedPopups:
                popup.click()

            nextLinks = self.driver.find_elements_by_xpath('//li[@class="currentPage"]/following-sibling::li')
            if len(nextLinks) == 0:
                break

            if nextLinks[0].text == previousLinkText:
                break

            print '  Jump next page', queryId, previousLinkText, '->', nextLinks[0].text, threading.current_thread()
            previousLinkText = nextLinks[0].text
            nextLinks[0].click()
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, xPathToWait)))

    def truncOrderId(self, orderId):
        m = re.search("\d", orderId)
        if m:
            return orderId[m.start():]
            # print "Digit found at position %d" % m.start()
        else:
            return orderId
            # print "No digit in that string"
