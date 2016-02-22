import traceback
import datetime
from datetime import *

import psycopg2

from Purchase import *
from PurchasesPostETL import *


class DBSaver:
    def __init__(self):
        self.conn = psycopg2.connect("dbname='MonitorPurchase' user='postgres' host='localhost' password='q1w2e3r4'")
        self.journalId = None

    def testDbConnecivity(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT * from tJournal""")
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            print row

    def logErr(self, msg, exc):
        (exc_type, exc_value, exc_traceback) = exc
        cur = self.conn.cursor()
        print "logErr:Exception:", (str(msg.encode('utf-8')), str(exc_type), str(exc_value),
                                    traceback.format_tb(exc_traceback))
        cur.execute("""insert into tErrorLog (message, exc_type, exc_value, exc_traceback) values (%s, %s, %s, %s)
                """, (
            str(msg.encode('utf-8'))[:500], str(exc_type)[:500], str(exc_value)[:500],
            traceback.format_tb(exc_traceback)))
        self.conn.commit()
        cur.close()

    def storePurchase(self, orderId, url):
        """
        returns Purchase structure for either existing or new Purchase
        """
        cur = self.conn.cursor()
        try:

            cur.execute(
                """select purchaseId, orderId, _url, _loadDate from tPurchase where orderId=%s and _url like %s """,
                [str(orderId), str('%' + url)])
            purchases = cur.fetchall()
            loadDate = None
            purchaseId = None
            if len(purchases) == 0:
                cur.execute("""select nextval('idGen')""")
                purchaseId = cur.fetchone()[0]
                cur.execute("""insert into tPurchase (purchaseId, orderId, _url) values
                (%s,%s,%s) """, (purchaseId, orderId[:35], url))
                print "created Purchase:", purchaseId, orderId, url
                loadDate = datetime.datetime(1900, 1, 1)
                self.conn.commit()
            else:
                purchaseId = purchases[0][0]
                loadDate = purchases[0][3]
                #print "Purchase exists:", purchaseId, orderId, url, loadDate
            p = Purchase()
            p.purchaseId = purchaseId
            p.orderId = orderId
            p._loadDate = loadDate
            p._url = url
            return p
        # except:
        #     traceback.print_tb(sys.exc_traceback)
        #     self.logErr("No Purchase: " + orderId, sys.exc_info())
        #     raise NameError("No Purchase: " + orderId)
        finally:
            cur.close()

    def storePurchaseData(self, purchaseId, dataDict):
        cur = self.conn.cursor()
        try:
            cur.execute("""DELETE FROM tPurchaseRawData where purchaseId=%s """, [purchaseId])

            for key, value in dataDict.iteritems():
                vKey = key[:500].encode('utf-8')
                vValue = value.encode('utf-8')
                vValue500 = value[:500].encode('utf-8')
                cur.execute(
                    """INSERT INTO tPurchaseRawData (purchaseId, keyName, textValue, textValue512 )
                        VALUES (%s, %s, %s, %s) """,
                    [purchaseId, vKey, vValue, vValue500])

            self.conn.commit()
        finally:
            cur.close()

    def storePurchaseContractData(self, purchaseContractId, dataDict):
        cur = self.conn.cursor()
        try:
            cur.execute("""DELETE FROM tContractRawData where purchaseContractId=%s """, [purchaseContractId])

            for key, value in dataDict.iteritems():
                vKey = key[:500].encode('utf-8')
                vValue = value.encode('utf-8')
                vValue500 = value[:500].encode('utf-8')
                cur.execute(
                    """INSERT INTO tContractRawData (purchaseContractId, keyName, textValue, textValue512 )
                        VALUES (%s, %s, %s, %s) """,
                    [purchaseContractId, vKey, vValue, vValue500])

            self.conn.commit()
        finally:
            cur.close()

    def storePurchaseFiles(self, purchaseId, purchases):
        cur = self.conn.cursor()
        try:
            for prcf in purchases:
                cur.execute(
                    """ SELECT purchaseFileId, purchaseId, url, title, filename, _loadDate  FROM tPurchaseFiles WHERE purchaseId=%s and url=%s and title=%s """,
                    [prcf.purchaseId, prcf.url.encode('utf-8'), prcf.title.encode('utf-8')])
                res = cur.fetchall()
                if len(res) < 1:
                    cur.execute("""select nextval('idGen')""")
                    purchaseFileId = cur.fetchone()[0]
                    cur.execute(
                        """ INSERT INTO tPurchaseFiles (purchaseFileId, purchaseId, url, title, filename) VALUES (%s, %s, %s, %s, %s) """,
                        [purchaseFileId, purchaseId, prcf.url.encode('utf-8'), prcf.title.encode('utf-8'),
                         prcf.filename.encode('utf-8')])
            self.conn.commit()
        # except Exception as ex:
        #     traceback.print_tb(sys.exc_traceback)
        #     traceback.print_last()
        #     self.logErr("Exception for purchaseId:" + str(purchaseId), sys.exc_info())
        #     self.conn.rollback()
        #     raise NameError("Exception for purchaseId:" + str(purchaseId))
        finally:
            cur.close()

    def storePurchaseContract(self, contract):
        cur = self.conn.cursor()
        try:

            cur.execute(
                """ SELECT purchaseContractId, purchaseId, url, customerName, _loadDate
                FROM tPurchaseContracts WHERE purchaseId=%s and url=%s and customerName=%s """,
                [contract.purchaseId, contract.url.encode('utf-8'), contract.customerName.encode('utf-8')])
            res = cur.fetchall()
            if len(res) < 1:
                cur.execute("""select nextval('idGen')""")
                purchaseContractId = cur.fetchone()[0]
                cur.execute(
                    """ INSERT INTO tPurchaseContracts
                    (purchaseContractId, purchaseId, contractNo, url, customerName, winnerName, priceT, pushishDateT)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """,
                    [purchaseContractId, contract.purchaseId, contract.contractNo.encode('utf-8'),
                     contract.url.encode('utf-8'), contract.customerName.encode('utf-8'),
                     contract.winnerName.encode('utf-8'), contract.priceT.encode('utf-8'),
                     contract.pushishDateT.encode('utf-8')])
            self.conn.commit()
        # except Exception as ex:
        #     traceback.print_tb(sys.exc_traceback)
        #     traceback.print_last()
        #     self.logErr("Exception for purchaseId:" + str(purchaseId), sys.exc_info())
        #     self.conn.rollback()
        #     raise NameError("Exception for purchaseId:" + str(purchaseId))
        finally:
            cur.close()

    def getQueryStrings(self):
        """
        :return: Array [Id,Text]
        """
        cur = self.conn.cursor()
        try:
            cur.execute(
                """ SELECT queryId, qText FROM tSourceQueries WHERE lastRun is null or lastRun<=%s""",
                [datetime.datetime.today() - timedelta(days=1)])

            rv = []
            res = cur.fetchall()
            for row in res:
                rv.append([row[0], row[1]])
            return rv
        finally:
            cur.close()

    def touchQuery(self, queryId):
        cur = self.conn.cursor()
        try:
            cur.execute(
                """ UPDATE tSourceQueries SET lastRun=%s WHERE  queryId=%s """,
                [datetime.datetime.today(), queryId])
            self.conn.commit()
        finally:
            cur.close()

    def touchPurchase(self, purchaseId):
        cur = self.conn.cursor()
        try:
            cur.execute(
                """ UPDATE tPurchase SET lastUpdate=%s WHERE  purchaseId=%s """,
                [datetime.datetime.today(), purchaseId])
            self.conn.commit()
        finally:
            cur.close()

    def touchPurchaseContract(self, purchaseContractId):
        cur = self.conn.cursor()
        try:
            cur.execute(
                """ UPDATE tPurchaseContracts  SET lastUpdate=%s WHERE  purchaseContractId=%s """,
                [datetime.datetime.today(), purchaseContractId])
            self.conn.commit()
        finally:
            cur.close()

    def getPurchases(self, depth=0):
        """
        :param depth: =0 - only new purchase requests
                    =1 - both new and older than 5 days
        :return:
        """
        cur = self.conn.cursor()
        try:
            sql = """ SELECT purchaseId, orderId, _url, _loadDate FROM tPurchase WHERE lastUpdate is null """
            prms = []
            if depth >= 1:
                sql += """ or lastUpdate<=%s """
                prms.append(datetime.datetime.today() - timedelta(days=3))
            cur.execute(sql, prms)

            rv = []
            res = cur.fetchall()
            for row in res:
                vPur = Purchase()
                vPur.purchaseId = row[0]
                vPur.orderId = row[1]
                vPur._url = row[2]
                vPur._loadDate = row[3]
                rv.append(vPur)

            return rv
        finally:
            cur.close()

    def getPurchaseContracts(self, depth=0):
        """
        :param depth: =0 - only new contracts
                    =1 - both new and older than 5 days
        :return:
        """
        cur = self.conn.cursor()
        try:
            sql = """ SELECT purchaseContractId, purchaseId, url, contractNo, customerName, winnerName, priceT, pushishDateT, _loadDate FROM tPurchaseContracts WHERE lastUpdate is null """
            prms = []
            if depth >= 1:
                sql += """ or lastUpdate<=%s """
                prms.append(datetime.datetime.today() - timedelta(days=3))
            cur.execute(sql, prms)

            rv = []
            res = cur.fetchall()
            for row in res:
                purchaseId = row[1]
                url = row[2]
                contractNo = row[3]
                customerName = row[4]
                winnerName = row[5]
                priceT = row[6]
                pushishDateT = row[7]
                vPurC = PurchaseContract(purchaseId, url, contractNo, customerName, winnerName, priceT, pushishDateT)
                vPurC.purchaseContractId = row[0]
                rv.append(vPurC)

            return rv
        finally:
            cur.close()

    def getOrganizations(self):
        """
        :return:
        """
        cur = self.conn.cursor()
        try:
            sql = """ SELECT orgId, inn, title, url_sbis, _loadDate  FROM tOrganization  WHERE inn is not null and (title is NULL or url_sbis is null) """
            cur.execute(sql)

            rv = []
            res = cur.fetchall()
            for row in res:
                vOrg = Organization()
                vOrg.orgId = row[0]
                vOrg.inn = row[1]
                vOrg.title = row[2]
                vOrg.url_sbis = row[3]
                vOrg._loadDate = row[4]
                rv.append(vOrg)

            return rv
        finally:
            cur.close()

    def postETL(self):
        PurchasesPostETL(self.conn).runPostETL()
