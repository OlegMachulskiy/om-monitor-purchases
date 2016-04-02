import re

# from selenium import webdriver
# from WebDrvManager import WebDrvManager
#
# from Purchase import *
# from PageParserPurchaseRequest import *
# from PageParserContract import *
# from PageParserSearchResults import *
# from OrganizationFinder import *
#
# from PageParserPurchaseBid import *
# import platform
#
#
# class ScrapZakupkiGovRu(WebDrvManager):
#     def __init__(self):
#         pass
#
#     def __del__(self):
#         WebDrvManager.__del__(self)
#
#     # def scrapSearchResults(self, dbSaver, queryId, scrapingUrl):
#     #     ppr = PageParserSearchResults(dbSaver, self.driver)
#     #     ppr.scrapSearchResults(queryId, scrapingUrl)
#
#     # def scrapOrderContent(self, dbSaver, vPurchase):
#     #     ppr = PageParserPurchaseRequest(dbSaver, self.driver)
#     #     ppr.scrapOrderContent(vPurchase)
#
#     # def scrapPurchaseContract(self, dbSaver, purchContr):
#     #     ppr = PageParserContract(dbSaver, self.driver)
#     #     ppr.scrapContract(purchContr)
#
#     # def lookupOrganizationInfo(self, dbSaver, vOrg):
#     #     orgf = OrganizationFinder(dbSaver, self.driver)
#     #     orgf.lookupOrganizationInfo(vOrg)
#
#     def scrapPurchaseBid(self, dbSaver, vBid):
#         ppb = PageParserPurchaseBid(dbSaver, self.driver)
#         ppb.scrapPurchaseBid(vBid)
