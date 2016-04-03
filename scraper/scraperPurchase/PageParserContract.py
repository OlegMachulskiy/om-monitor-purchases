import re
from urllib2 import HTTPError
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.common.by import By

from selenium import webdriver


class PageParserContract:
    def __init__(self, dbSaver, driver):
        self.dbSaver = dbSaver
        self.driver = driver

    def readTabPurchaseContractData(self):
        # fullTextHTML = self.driver.page_source
        # open("file02.html", "w").write(fullTextHTML.encode('utf-8'))
        d = {}
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="noticeTabBoxWrapper"]/table/tbody/tr')))

        dataTRs = self.driver.find_elements_by_xpath(
            '//div[@class="noticeTabBoxWrapper"]/table/tbody/tr')
        if len(dataTRs) < 1:
            raise Exception("Page returned has no data:", self.driver.current_url)

        for dtr in dataTRs:
            tds = dtr.find_elements_by_xpath("td")
            if len(tds) > 1:
                vKey = tds[0].text
                vValue = tds[1].text
                d[vKey] = vValue

        dataTRs = self.driver.find_elements_by_xpath(
            '//table[@class="participantInfoTable"]/tbody/tr')
        for dtr in dataTRs:
            tds = dtr.find_elements_by_xpath("td")
            if len(tds) > 1:
                vKey = tds[0].text
                vValue = tds[1].text
                d["participantInfoTable:" + vKey] = vValue

        return d

    def scrapContract(self, vPurchContract):
        # do the following for purchases only once per sevral days
        # ActionChains(self.driver).key_down(Keys.CONTROL).click(orderA).key_up(Keys.CONTROL).perform()
        # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        #
        # self.driver.switch_to_window(main_window)
        print "scrapContract:", vPurchContract
        self.driver.get(vPurchContract.url)
        contractDataMap = self.readTabPurchaseContractData()
        self.dbSaver.storePurchaseContractData(vPurchContract.purchaseContractId, contractDataMap)
