# -*- coding: utf-8 -*-

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
        if isinstance(exc, Exception):
            # eee = Exception
            (exc_type, exc_value, exc_traceback) = (exc.__class__, exc.message, traceback.extract_stack())
        else:  # sys.exc_info() contains it
            (exc_type, exc_value, exc_tracebackObj) = exc
            exc_traceback = traceback.extract_tb(exc_tracebackObj)
        cur = self.conn.cursor()
        try:
            print "logErr:Exception:", (str(msg.encode('utf-8')), str(exc_type), str(exc_value))
            cur.execute("""insert into tErrorLog (message, exc_type, exc_value, exc_traceback) values (%s, %s, %s, %s)
                    """, (
                str(msg.encode('utf-8'))[:500], str(exc_type)[:500], str(exc_value)[:500],
                traceback.format_list(exc_traceback)))
            self.conn.commit()
        finally:
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
                # print "Purchase exists:", purchaseId, orderId, url, loadDate
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
                prms.append(datetime.datetime.today() - timedelta(days=5))
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

    def getPurchase(self, purchaseId):

        cur = self.conn.cursor()
        try:
            cur.execute(""" SELECT purchaseId, orderId, _url, _loadDate FROM tPurchase WHERE purchaseId=%s""",
                        [purchaseId])

            row = cur.fetchone()
            vPur = Purchase()
            vPur.purchaseId = row[0]
            vPur.orderId = row[1]
            vPur._url = row[2]
            vPur._loadDate = row[3]

            return vPur
        finally:
            cur.close()

    def getPurchaseContracts(self, depth=0, purchaseContractId=None):
        """
        :param depth: =0 - only new contracts
                    =1 - both new and older than 5 days
        :return:
        """
        cur = self.conn.cursor()
        try:
            if purchaseContractId == None:
                sql = """ SELECT purchaseContractId, purchaseId, url, contractNo, customerName, winnerName, priceT, pushishDateT, _loadDate FROM tPurchaseContracts WHERE lastUpdate is null """
                prms = []
                if depth >= 1:
                    sql += """ or lastUpdate<=%s """
                    prms.append(datetime.datetime.today() - timedelta(days=5))
                cur.execute(sql, prms)
            else:
                sql = """ SELECT purchaseContractId, purchaseId, url, contractNo, customerName, winnerName, priceT, pushishDateT, _loadDate FROM tPurchaseContracts WHERE purchaseContractId=%s """
                cur.execute(sql, [purchaseContractId])

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

    def getOrganizations(self, vConditions=None, vParams=[]):
        """
        :return:
        """
        cur = self.conn.cursor()
        try:
            sql = """
                select tPartner.partnerId , tPartner.inn, tPartner.p_name, tPartner._loadDate,
                        tOrganization.orgFullName, tOrganization.directorName, tOrganization.directorPosition,
                        tOrganization.address, tOrganization.description, tOrganization.url_sbis
                FROM tPartner JOIN tOrganization  ON tPartner.partnerId = tOrganization.partnerId """
            if vConditions != None:
                sql = sql + " WHERE " + vConditions
            cur.execute(sql, vParams)

            rv = []
            res = cur.fetchall()
            for row in res:
                vOrg = Organization()
                vOrg.partnerId = row[0]
                vOrg.inn = row[1]
                vOrg.p_name = row[2]
                vOrg._loadDate = row[3]
                vOrg.orgFullName = row[4]
                vOrg.directorName = row[5]
                vOrg.directorPosition = row[6]
                vOrg.address = row[7]
                vOrg.description = row[8]
                vOrg.url_sbis = row[9]
                rv.append(vOrg)

            return rv
        finally:
            cur.close()

    def getOrganizationPartnerIdByINN(self, inn):
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT partnerId FROM tPartner WHERE inn=%s", [inn])
            rows = cur.fetchall()
            if len(rows) > 0:
                return rows[0][0]

            cur.execute("""select nextval('idGen')""")
            partnerId = cur.fetchone()[0]
            cur.execute("INSERT INTO tPartner (partnerId, inn) VALUES (%s, %s)", [partnerId, inn])
            cur.execute("INSERT INTO tOrganization (partnerId) VALUES (%s)", [partnerId])
            self.conn.commit()
            return partnerId
        finally:
            cur.close()

    def storeOrganization(self, vOrg):
        cur = self.conn.cursor()
        try:
            cur.execute("UPDATE tPartner SET inn=%s, p_name=%s WHERE partnerId=%s",
                        [vOrg.inn, vOrg.p_name, vOrg.partnerId])

            cur.execute(
                "UPDATE tOrganization "
                "SET orgFullName=%s, directorName=%s, directorPosition=%s, address=%s, description=%s, url_sbis=%s "
                "WHERE partnerId=%s",
                [vOrg.orgFullName, vOrg.directorName, vOrg.directorPosition, vOrg.address, vOrg.description,
                 vOrg.url_sbis, vOrg.partnerId])

            self.conn.commit()
        finally:
            cur.close()

    def postETL(self):
        PurchasesPostETL(self.conn).runPostETL()

    def storePerson(self, vPerson):
        cur = self.conn.cursor()
        try:
            if vPerson.partnerId == None:
                cur.execute("SELECT partnerId FROM tPartner WHERE p_name=%s ", [vPerson.p_name])
                rows = cur.fetchall()
                if len(rows) < 1:
                    cur.execute("""select nextval('idGen')""")
                    vPerson.partnerId = cur.fetchone()[0]
                    cur.execute("INSERT INTO tPartner (partnerId, inn, p_name, category) VALUES (%s, %s, %s, 'P')",
                                [vPerson.partnerId, vPerson.inn, vPerson.p_name])
                else:
                    vPerson.partnerId = rows[0][0]

            cur.execute("UPDATE tPartner SET inn=%s, p_name=%s, category='P' WHERE partnerId=%s",
                        [vPerson.inn, vPerson.p_name, vPerson.partnerId])

            self.conn.commit()
            return vPerson
        finally:
            cur.close()

    def storePartnerRelation(self, party1Id, party2Id, title):
        cur = self.conn.cursor()
        try:
            cur.execute(
                "SELECT partnerId1, partnerId2, title, _loadDate FROM tPartnerRelation WHERE partnerId1=%s AND partnerId2=%s",
                [party1Id, party2Id])
            res = cur.fetchall()
            if len(res) > 0:
                cur.execute(
                    "UPDATE tPartnerRelation SET title=%s WHERE partnerId1=%s AND partnerId2=%s",
                    [title, party1Id, party2Id])
            else:
                cur.execute(
                    "INSERT INTO tPartnerRelation (partnerId1, partnerId2, title) VALUES (%s, %s, %s)",
                    [party1Id, party2Id, title])
            self.conn.commit()
        finally:
            cur.close()

    # def pushPartnerURLQueue(self, url_sbis):
    #     cur = self.conn.cursor()
    #     try:
    #         cur.execute("INSERT INTO tPartnerURLQueue (url_sbis) VALUES (%s)", [url_sbis])
    #         self.conn.commit()
    #     finally:
    #         cur.close()
    #
    # def pullPartnerURLQueue(self):
    #     cur = self.conn.cursor()
    #     try:
    #         rv = []
    #         cur.execute("SELECT DISTINCT url_sbis FROM tPartnerURLQueue WHERE url_sbis IS NOT NULL")
    #         rows = cur.fetchall()
    #         for row in rows:
    #             rv.append(row[0])
    #         cur.execute("DELETE FROM tPartnerURLQueue")
    #         self.conn.commit()
    #     finally:
    #         cur.close()

    def storePurchaseBid(self, purchaseId, bidUrl):
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT bidId FROM tPurchaseBid WHERE purchaseId=%s AND url=%s", [purchaseId, bidUrl])
            rows = cur.fetchall()
            if len(rows) > 0:
                return rows[0][0]
            else:
                cur.execute("""select nextval('idGen')""")
                bidId = cur.fetchone()[0]
                cur.execute("INSERT INTO tPurchaseBid (bidId, purchaseId, url) VALUES (%s, %s, %s)",
                            [bidId, purchaseId, bidUrl])
                self.conn.commit()
                return bidId
        finally:
            cur.close()

    def getPurchaseBids(self):
        cur = self.conn.cursor()
        try:
            cur.execute(
                """ SELECT bidId, purchaseId, url, partnerId FROM tPurchaseBid
                WHERE partnerId IS NULL
                    OR bidId NOT IN (SELECT DISTINCT bidId FROM tPurchaseBidRawData)""",
                [datetime.datetime.today() - timedelta(days=5)])
            rows = cur.fetchall()
            rv = []
            for row in rows:
                bid = PurchaseBid()
                bid.bidId = row[0]
                bid.purchaseId = row[1]
                bid.url = row[2]
                bid.partnerId = row[3]
                rv.append(bid)
            return rv
        finally:
            cur.close()

    def storePurchaseBidRawData(self, bidId, dataDict):
        cur = self.conn.cursor()
        try:
            cur.execute("""DELETE FROM tPurchaseBidRawData where bidId=%s """, [bidId])

            for key, value in dataDict.iteritems():
                vKey = key[:500].encode('utf-8')
                vValue = value.encode('utf-8')
                vValue500 = value[:500].encode('utf-8')
                cur.execute(
                    """INSERT INTO tPurchaseBidRawData (bidId, keyName, textValue, textValue512 )
                        VALUES (%s, %s, %s, %s) """,
                    [bidId, vKey, vValue, vValue500])

            self.conn.commit()
        finally:
            cur.close()

    def updatePurchaseBidData(self, bidId):
        cur = self.conn.cursor()
        try:
            cur.execute("""
            insert into tPartner (partnerId, inn, category)
            (select nextval('idGen'), inn, 'O' from  (select distinct textValue512 as inn
                from tPurchaseBidRawData tbrd join tPurchaseBid tb ON tbrd.bidId=tb.bidId
                WHERE keyName='ИНН' and tb.bidId=%s) tpc
            WHERE not exists (select * from tPartner  tpd1 where tpd1.inn = tpc.inn) and inn is not null)
             """, [bidId])

            cur.execute(""" UPDATE tPurchaseBid ubd SET partnerId=
                (select distinct tp.partnerId
                from tPurchaseBidRawData tbrd
                join tPurchaseBid tb ON tbrd.bidId=tb.bidId AND keyName='ИНН'
                JOIN tPartner tp ON tp.inn = tbrd.textValue512
                            and tb.bidId=ubd.bidId
                    LIMIT 1) WHERE bidId=%s """, [bidId])

            self.conn.commit()
        finally:
            cur.close()


    def storeHTTPProxyResult(self, proxy, timeout, result):
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO tHTTPProxyResult (proxy, timeout, result) VALUES (%s, %s, %s)",
                        [proxy, timeout, result[:127]])
            self.conn.commit()
        finally:
            cur.close()
