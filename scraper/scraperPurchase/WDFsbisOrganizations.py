# -*- coding: utf-8 -*-

##############################################################################################################
### read organizations details from SBIS website
##############################################################################################################

from DBSaver import *
from OrganizationFinder import *
from AbstractWorkerDataFacade import *


class WDFsbisOrganizations(AbstractWorkerDataFacade):
    def getScrapingEntitiesFromDBS(self, dbSaver):
        # raise Exception("method getScrapingEntitiesFromDBS must be implemented in a runner class")
        return dbSaver.getOrganizations(" (p_name IS NULL AND inn IS NOT NULL)")

    def runScrapingForEntity(self, dbSaver, webDriverM, scrapingItem):
        # raise Exception("method runScrapingForEntity must be implemented in a runner class")
        # for example:
        # scraper.scrapOrderContent(dbSaver, scrapingItem)
        # dbSaver.touchPurchase(scrapingItem.purchaseId)
        orgf = OrganizationFinder(dbSaver, webDriverM.driver)
        orgf.lookupOrganizationInfo(scrapingItem)

        print "####### DONE FOR ORG ", scrapingItem.partnerId, " by ", threading.current_thread(), time.time()

    def getSIID(self, scrapingItem):
        return "sbis" + str(scrapingItem.partnerId)

    def defaultHttpTimeout(self):
        return 60


if __name__ == "__main__":
    df = WDFsbisOrganizations()
    dbSaver = DBSaver()
    wdm = WDFsbisOrganizations(useFirefoxDriver=True)
    queue = df.getScrapingEntitiesFromDBS(dbSaver)
    for item in queue:
        df.runScrapingForEntity(dbSaver, wdm, item)
