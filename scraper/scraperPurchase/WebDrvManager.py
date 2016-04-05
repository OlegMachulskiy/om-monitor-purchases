# -*- coding: utf-8 -*-

from ProxyFactory import *
from selenium import webdriver
from urllib2 import HTTPError

class WebDrvManager:
    def __init__(self, useProxy=True, defaultHttpTimeout=30, useFirefoxDriver=False):
        self.proxyxAddr = "No_Proxy"
        try:
            proxyParams = []
            if useFirefoxDriver:
                self.driver = webdriver.Firefox()
            else:
                if useProxy:
                    self.proxyxAddr = ProxyFactory().getRandomProxy()
                    proxyParams = ["--proxy=" + self.proxyxAddr]

                # self.driver = webdriver.PhantomJS("C:/usr/phantomjs-2.1.1-windows/bin/phantomjs.exe",
                #                                   service_args=proxyParams)

                if platform.system() == 'Windows':
                    self.driver = webdriver.PhantomJS("C:/usr/phantomjs-2.1.1-windows/bin/phantomjs.exe",
                                                      service_args=proxyParams)
                else:
                    self.driver = webdriver.PhantomJS("/opt/phantomjs-2.1.1-linux-i686/bin/phantomjs",
                                                      service_args=proxyParams)

                self.driver.implicitly_wait(defaultHttpTimeout)
                self.driver.set_page_load_timeout(defaultHttpTimeout)

                # open("file00.html", "w").write(unicode(self.driver.page_source).encode('utf-8'))
        except HTTPError as e:
            traceback.print_last()
            # print(e)
            raise (e)
        else:
            print "Created webDriver:", self.driver, proxyParams
        # return prxAddr

    def __del__(self):
        if self.driver != None:
            self.driver.quit()
