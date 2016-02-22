# -*- coding: utf-8 -*-

import re
from urllib2 import HTTPError

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class OrganizationFinder:
    def __init__(self, dbSaver, driver):
        self.dbSaver = dbSaver
        self.driver = driver

    def lookupOrganizationInfo(self, vOrg):
        # do the following for purchases only once per sevral days
        # ActionChains(self.driver).key_down(Keys.CONTROL).click(orderA).key_up(Keys.CONTROL).perform()
        # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        #
        # self.driver.switch_to_window(main_window)
        print "lookupOrganizationInfo:", vOrg
        # self.driver.get(vPurchContract.url)
        # contractDataMap = self.readTabPurchaseContractData()
        # self.dbSaver.storePurchaseContractData(vPurchContract.purchaseContractId, contractDataMap)
        elem = self.driver.find_element_by_xpath('//input[@name="text"]')
        elem.send_keys("sbis ИНН " + vOrg.inn)
        elem.send_keys(Keys.RETURN)
        hrefs = self.driver.find_elements_by_xpath('//h2[class="serp-item__title"]/a')
        hrefs[0].click()

