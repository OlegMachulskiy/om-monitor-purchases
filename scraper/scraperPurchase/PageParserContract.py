# -*- coding: utf-8 -*-


import sys
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0

from Purchase import ContractSupplier


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

        # dataTRs = self.driver.find_elements_by_xpath(
        #     '//table[@class="participantInfoTable"]/tbody/tr')
        # for dtr in dataTRs:
        #     tds = dtr.find_elements_by_xpath("td")
        #     if len(tds) > 1:
        #         vKey = tds[0].text
        #         vValue = tds[1].text
        #         d["participantInfoTable:" + vKey] = vValue

        return d

    def readTabSuppliers(self, vPurchContract):
        trS = self.driver.find_elements_by_xpath('//table[@id="supplier"]/tbody/tr')
        for sTR in trS:
            tdS = sTR.find_elements_by_xpath("td")
            if len(tdS) > 0:
                inn = tdS[4].text
                sA = tdS[0].find_element_by_xpath('a')
                supplName = sA.text
                supplUrl = sA.get_attribute('href')
                contractSupplier = ContractSupplier(vPurchContract.purchaseContractId, inn, supplierName=supplName, url=supplUrl)
                self.dbSaver.storeContractSupplier(contractSupplier)

    def scrapContract(self, vPurchContract):
        # do the following for purchases only once per sevral days
        # ActionChains(self.driver).key_down(Keys.CONTROL).click(orderA).key_up(Keys.CONTROL).perform()
        # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        #
        # self.driver.switch_to_window(main_window)
        print "scrapContract:", vPurchContract
        self.driver.get(vPurchContract.url)

        contractDataMap = self.readTabPurchaseContractData()

        moreDataTab = self.driver.find_elements_by_xpath('//table[@class="contentTabsWrapper"]//td/span[text()="Информация о предмете договора"]')
        if len(moreDataTab) > 0:
            moreDataTab[0].click()
            extendedMap = self.readTabPurchaseContractData()
            contractDataMap.update(extendedMap)
        else:
            pass  ### no results tab present on the page

        self.dbSaver.storePurchaseContractData(vPurchContract.purchaseContractId, contractDataMap)

        suppliersTab = self.driver.find_elements_by_xpath('//table[@class="contentTabsWrapper"]//td/span[text()="Информация о поставщиках"]')
        try:
            if len(suppliersTab) > 0:
                suppliersTab[0].click()
                self.readTabSuppliers(vPurchContract)
            else:
                pass  ### no results tab present on the page
        except Exception as ex:
            traceback.print_exc()
            self.dbSaver.logErr("Warning: cannot read  SUPPLIER_RESULTS tab:" + vPurchContract.url, sys.exc_info())
