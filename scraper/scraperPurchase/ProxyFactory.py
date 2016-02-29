# -*- coding: utf-8 -*-

import random
# from numpy.random import choice

from selenium import webdriver

from DBSaver import *
import bisect

class ProxyFactory:
    plist = [
        "166.70.91.1:8080",
        "139.193.134.243:8080",
        "151.236.63.217:3128",
        "46.39.205.1:8080",
        "177.55.255.250:8080",
        "124.89.33.60:9999",
        "124.206.236.171:3128",
        "180.73.0.2:83",
        "124.207.14.155:3128",
        "120.50.11.146:8080",
        "165.138.66.247:8080",
        "123.146.128.15:3128",
        "150.242.104.218:8080",
        "186.121.212.90:80",
        "115.124.72.78:8585",
        "177.136.113.38:8080",
        "122.156.230.178:3128",
        "123.57.133.112:8080",
        "123.65.217.151:9797",
        "122.226.156.220:3128",
        "103.254.167.39:8080",
        "111.38.174.99:3128",
        "109.121.146.159:8080",
        "123.7.115.141:9797",
        "103.233.119.237:8080",
        "103.54.220.154:8080",
        "181.143.238.122:8080",
        "119.29.97.169:3128",
        "116.31.76.196:3128",
        "107.17.100.254:8080",
        "120.198.231.21:8081",
        "41.72.201.78:3128",
        "120.198.231.85:81",
        "118.163.108.104:3128",
        "41.79.60.202:8080",
    ]

    def __init(self):
        pass



# with stats as (
# 	select proxy, avg(timeout) as avg_ok, count(timeout) as count_ok, 0 as avg_err, 0 as count_err from tHTTPProxyResult where result='Success' group by proxy
# 	union all
# 	select proxy, 0 as avg_ok, 0 as count_ok, avg(timeout)  as avg_err, count(timeout) as  count_err from tHTTPProxyResult where result is NULL OR result <>'Success' group by proxy
# 	union all
# 	select proxy, 10000 as avg_ok, 1 as count_ok, 10000 as avg_err, 1 as count_err from tHTTPProxies where proxy not in (select distinct proxy from tHTTPProxyResult)
# ), stats1 as (
# 	select proxy, sum(avg_ok) as avg_ok, sum(count_ok) as count_ok, sum(avg_err) as avg_err, sum(count_err) as count_err from stats group by proxy
# ), weighted as
# (
# 	select proxy, avg_ok, count_ok, avg_err, count_err, count_err/count_ok as error_rate, 1000000/(avg_ok+avg_err)  as weight
# 	from stats1 where count_ok > 0
#
# ) select proxy , weight/( 1 + error_rate) as weight1, avg_ok  from weighted
# where proxy <> 'No_Proxy'
# order by  weight1 desc


    def getRandomProxy(self, fromDb=True):
        if fromDb:
            dbs = DBSaver()
            cur = dbs.conn.cursor()
            try:
                cur.execute("""

with stats as (
	select proxy, avg(timeout) as avg_ok, count(timeout) as count_ok, 0 as avg_err, 0 as count_err from tHTTPProxyResult where result='Success' group by proxy
	union all
	select proxy, 0 as avg_ok, 0 as count_ok, avg(timeout)  as avg_err, count(timeout) as  count_err from tHTTPProxyResult where result is NULL OR result <>'Success' group by proxy
	union all
	select proxy, 10000 as avg_ok, 1 as count_ok, 10000 as avg_err, 1 as count_err from tHTTPProxies where proxy not in (select distinct proxy from tHTTPProxyResult)
), stats1 as (
	select proxy, sum(avg_ok) as avg_ok, sum(count_ok) as count_ok, sum(avg_err) as avg_err, sum(count_err) as count_err from stats group by proxy
), weighted as
(
	select proxy, avg_ok, count_ok, avg_err, count_err, (count_err)/(count_ok) as error_rate, 1000000/(avg_ok+avg_err)  as weight
	from stats1
	where count_ok > 0
) select proxy , (weight/( 1 + error_rate))^2 as weight1, avg_ok , * from weighted
where proxy <> 'No_Proxy'
order by  weight1 desc

                """);
                res = cur.fetchall()
                self.plist = []
                self.weights = []
                for prx in res:
                    self.plist.append(prx[0])
                    self.weights.append(float(prx[1]))

                idx = self.weighted_choice_king(self.weights)
                return self.plist[idx]

            finally:
                cur.close()


    def updateProxyList01(self):
        self.driver = webdriver.PhantomJS("C:/usr/phantomjs-2.1.1-windows/bin/phantomjs.exe")
        try:
            rv = []
            pUrl = 'http://www.ultraproxies.com/'
            print "updating proxies from:", pUrl
            self.driver.get(pUrl)
            rows = self.driver.find_elements_by_xpath('//table[@class="proxy"]/tbody/tr')
            for row in rows:
                ips = row.find_elements_by_xpath('td[@class="ip"]')
                ports = row.find_elements_by_xpath('td[@class="port"]')
                if len(ips) > 0 and len(ports) > 0:
                    addr = ips[0].text + ports[0].text
                    rv.append(addr.encode("utf-8"))
            print "DONE: updating proxies from:", pUrl, len(rv)
            return set(rv)
        finally:
            self.driver.close()

    def updateProxyList02(self):
        self.driver = webdriver.PhantomJS("C:/usr/phantomjs-2.1.1-windows/bin/phantomjs.exe")
        try:
            rv = []
            pUrl = 'https://www.us-proxy.org/'
            print "updating proxies from:", pUrl
            self.driver.get(pUrl)
            rows = self.driver.find_elements_by_xpath('//table[@id="proxylisttable"]/tbody/tr')
            for row in rows:
                tds = row.find_elements_by_xpath('td')
                if len(tds) > 4:
                    addr = tds[0].text + ':' + tds[1].text
                    rv.append(addr.encode("utf-8"))
            print "DONE: updating proxies from:", pUrl, len(rv)
            return set(rv)
        finally:
            self.driver.close()

    def updateProxyList03(self):
        self.driver = webdriver.PhantomJS("C:/usr/phantomjs-2.1.1-windows/bin/phantomjs.exe")
        try:
            rv = []
            pUrl = 'http://spys.ru/proxylist/'
            print "updating proxies from:", pUrl
            self.driver.get(pUrl)

            select = self.driver.find_element_by_xpath('//select[@id="xpp"]')
            allOptions = select.find_elements_by_xpath("option")
            for option in allOptions:
                if option.text == u'200':
                    option.click()
                    break

            rows = self.driver.find_elements_by_xpath('//tr[@class="spy1xx" or @class="spy1x"]')
            for row in rows:
                tds = row.find_elements_by_xpath('td/font[@class="spy14"]')
                if len(tds) > 0:
                    addr = tds[0].text
                    rv.append(addr.encode("utf-8"))
            print "DONE: updating proxies from:", pUrl, len(rv)
            return set(rv)
        finally:
            self.driver.close()

    def updateProxyList04(self):
        self.driver = webdriver.PhantomJS("C:/usr/phantomjs-2.1.1-windows/bin/phantomjs.exe")
        try:
            rv = []
            pUrl = 'https://proxy-list.org/english/index.php'
            print "updating proxies from:", pUrl
            self.driver.get(pUrl)

            vContinue = True
            while vContinue:
                rows = self.driver.find_elements_by_xpath('//div[@class="table"]/ul/li[@class="proxy"]')
                for row in rows:
                    addr = row.text
                    if len(addr) > 0:
                        rv.append(addr.encode("utf-8"))

                nextLink = self.driver.find_elements_by_xpath('//div[@class="table-menu"]/a[@class="next"]')
                if len(nextLink) > 0:
                    nextLink[0].click()
                    print "next page Clicked"
                else:
                    vContinue = False

            print "DONE: updating proxies from:", pUrl, len(rv)
            return set(rv)
        finally:
            self.driver.close()

    def updateProxiesInDB(self):
        lst = []
        lst.extend(self.updateProxyList04())
        lst.extend(self.updateProxyList03())
        lst.extend(self.updateProxyList01())
        lst.extend(self.updateProxyList02())
        lst.extend(self.plist)
        proxies = set(lst)
        print "Total proxies to use:", len(proxies)
        dbs = DBSaver()
        cur = dbs.conn.cursor()
        try:
            cur.execute("DELETE FROM tHTTPProxies");
            for prx in proxies:
                cur.execute("INSERT INTO tHTTPProxies (proxy) VALUES (%s);", [prx]);
            dbs.conn.commit()
        finally:
            cur.close()

    def weighted_choice_king(self, weights):
        total = 0
        winner = 0
        for i, w in enumerate(weights):
            total += w
            if random.random() * total < w:
                winner = i
        return winner

if __name__ == '__main__':
    ProxyFactory().updateProxiesInDB()
