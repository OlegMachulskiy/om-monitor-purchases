# -*- coding: utf-8 -*-

import re
import threading
from urllib2 import HTTPError

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.common.by import By

from scraperPurchase import Person


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
        print "lookupOrganizationInfo:", vOrg, threading.current_thread()
        # self.driver.get(vPurchContract.url)
        # contractDataMap = self.readTabPurchaseContractData()
        # self.dbSaver.storePurchaseContractData(vPurchContract.purchaseContractId, contractDataMap)
        vOrg.url_sbis = "https://sbis.ru/contragents/" + vOrg.inn

        self.driver.get(vOrg.url_sbis)
        element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="cCard__MainReq"]')))

        vOrg.p_name = element.find_element_by_xpath('div[@class="cCard__MainReq-Name"]/h1').text
        owners = []
        innCandidates = element.find_elements_by_xpath(
            'div[@class="cCard__MainReq-Right"]/div/div/div[@class="cCard__MainReq-Right-Req-Label"]')
        for innCandidate in innCandidates:
            if innCandidate.text == u"ИНН":
                vOrg.inn = innCandidate.find_element_by_xpath('following-sibling::div').text
                break

        legalNames = element.find_elements_by_xpath('div[@itemprop="legalName"]')

        if len(legalNames) > 0:  # Юрлицо
            vOrg.orgFullName = legalNames[0].text

            dirNames = self.driver.find_elements_by_xpath(
                '//div[@class="cCard__Director"]/div[@class="cCard__Director-Name"]')
            if len(dirNames) > 0:
                vOrg.directorName = dirNames[0].text
                dirPos = self.driver.find_elements_by_xpath(
                    '//div[@class="cCard__Director"]/div[@class="cCard__Director-Position"]')
                if len(dirPos)>0:
                    vOrg.directorPosition = dirPos[0].text
                else:
                    vOrg.directorPosition = None
                owners.append([vOrg.directorName, vOrg.directorPosition, None])
            else:
                vOrg.directorName = None
                vOrg.directorPosition = None

            contactsAddress = self.driver.find_elements_by_xpath('//div[@class="cCard__Contacts-Address"]')
            if len(contactsAddress)>0:
                vOrg.address = contactsAddress[0].text
            else:
                vOrg.address = None

            ownerDivs = self.driver.find_elements_by_xpath(
                '//div[@class="cCard__Owners-OwnerList"]/div[@class="cCard__Owners-OwnerList-Name"]')

            for ownerDiv in ownerDivs:
                details = ownerDiv.find_element_by_xpath('following-sibling::div')
                href = None

                hrefs = ownerDiv.find_elements_by_xpath("a")
                if len(hrefs) > 0:
                    href = hrefs[0].get_attribute('href')
                    # self.dbSaver.pushPartnerURLQueue(href)
                owners.append([ownerDiv.text, details.text, href])

        else:  # ИПшник
            vOrg.orgFullName = vOrg.p_name
            vOrg.directorName = None
            vOrg.directorPosition = None
            vOrg.address = None

        vOrg.description = self.driver.find_element_by_xpath('//div[@class="cCard__CompanyDescription"]').text

        self.dbSaver.storeOrganization(vOrg)
        # print orgName, orgFullName, directorName, directorPosition, address, owners, description
        for owner in owners:
            vPerson = Person()
            vPerson.p_name = owner[0]
            if owner[2] == None:  ## there was no hyperlink
                vPerson = self.dbSaver.storePerson(vPerson)
                self.dbSaver.storePartnerRelation(vOrg.partnerId, vPerson.partnerId, owner[1])
            else:  # owner was a link to the page of another legal entity like "https://sbis.ru/contragents/7710542402/771001001"
                parsedInn = owner[2].split("/")[4]
                # print "https://sbis.ru/contragents/7710542402/771001001".split("/")
                newOrgId = self.dbSaver.getOrganizationPartnerIdByINN(parsedInn)
                self.dbSaver.storePartnerRelation(vOrg.partnerId, newOrgId , owner[1])

