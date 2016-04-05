# -*- coding: utf-8 -*-

import urllib
from unidecode import unidecode
from AbstractWorkerDataFacade import *
from PageParserSearchResults import *
from WebDrvManager import *

# http://cbr.ru/credit/transparent.asp
from PdfTextExtractor import PdfTextExtractor


class WDFbanksListCBR(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        # raise Exception("method getScrapingEntitiesFromDBS must be implemented in a runner class")
        wdm = WebDrvManager(useProxy=False)
        rvCBRids = []
        try:
            wdm.driver.get('http://cbr.ru/credit/transparent.asp')
            bLinks = wdm.driver.find_elements_by_xpath('//table[@class="data"]/tbody/tr/td/a[contains(@href, "info(")]')
            for theA in bLinks:
                sid = theA.get_attribute("href")
                sid = sid[len('javascript:info('):-1]
                rvCBRids.append(sid)
        finally:
            del wdm
        return rvCBRids

    def runScrapingForEntity(self, dbSaver, webDriverM, scrapingItem):
        url = 'http://cbr.ru/credit/coinfo.asp?id=' + scrapingItem
        webDriverM.driver.get(url)
        trS = webDriverM.driver.find_elements_by_xpath('//table[@class=" nodata"]/tbody/tr')
        dataMap = {}
        for theR in trS:
            tdS = theR.find_elements_by_xpath("td")
            theK = tdS[0].text
            theV = tdS[1].text
            dataMap[theK] = theV

        titles = webDriverM.driver.find_elements_by_xpath('//h1[@id="__pagetitle_h1"]')
        if len(titles) > 0:
            dataMap['Bank-Title'] = titles[0].text

        pdfs = webDriverM.driver.find_elements_by_xpath('//div/p[@class="file PDF small_icon"]/a')
        if len(pdfs) > 0:
            pdfText = PdfTextExtractor().pdf2text(pdfs[0].get_attribute("href"))
            dataMap['Bank-Structure'] = unicode(pdfText, "utf-8")

        links = webDriverM.driver.find_elements_by_xpath('//div[@class="org_info"]/div[@class="links"]')
        if len(links) > 0:
            dataMap['Bank-Links'] = links[0].text

        dbSaver.updateBankRegData(bankId=scrapingItem, bankData=dataMap, updated=datetime.datetime.now())

        pass
        print "####### DONE FOR Bank ", scrapingItem, " by ", threading.current_thread(), ' at ', datetime.datetime.now()

    def getSIID(self, scrapingItem):
        return "cbrb" + scrapingItem

    def useProxy(self):
        return False


if __name__ == "__main__":
    df = WDFbanksListCBR()
    dbSaver = DBSaver()

    queue = df.getScrapingEntitiesFromDBS(dbSaver)
    # queue = [u'450000036', u'450000790', u'450000370', u'450000785', u'920000004', u'920000023']
    print queue
    wdm = WebDrvManager(useFirefoxDriver=True)
    for item in queue:
        df.runScrapingForEntity(dbSaver, wdm, item)
    del wdm
