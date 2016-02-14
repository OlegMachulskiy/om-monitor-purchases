import sys
import traceback
from datetime import *

import psycopg2

from Purchase import *


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
                loadDate = datetime(1900, 1, 1)
                self.conn.commit()
            else:
                purchaseId = purchases[0][0]
                loadDate = purchases[0][3]
                print "Purchase exists:", purchaseId, orderId, url, loadDate
            p = Purchase()
            p.purchaseId = purchaseId
            p.orderId = orderId
            p._loadDate = loadDate
            p._url = url
            return p
        except:
            traceback.print_tb(sys.exc_traceback)
            self.logErr("No Purchase: " + orderId, sys.exc_info())
            raise NameError("No Purchase: " + orderId)
        finally:
            cur.close()

    def storePurchaseData(self, purchaseId, dataDict):
        cur = self.conn.cursor()
        try:
            cur.execute("""DELETE FROM tPurchaseData where purchaseId=%s """, [purchaseId])

            for key, value in dataDict.iteritems():
                vKey = key[:500].encode('utf-8')
                vValue = value.encode('utf-8')
                vValue500 = value[:500].encode('utf-8')
                cur.execute(
                    """INSERT INTO tPurchaseData (purchaseId, keyName, textValue, textValue512 )
                        VALUES (%s, %s, %s, %s) """,
                    [purchaseId, vKey, vValue, vValue500])

            self.conn.commit()
        except:
            traceback.print_tb(sys.exc_traceback)
            self.logErr("PurchaseData Exception for purchaseId:" + str(purchaseId), sys.exc_info())
            self.conn.rollback()
            raise NameError("PurchaseData Exception for purchaseId:" + str(purchaseId))
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
        except Exception as ex:
            traceback.print_tb(sys.exc_traceback)
            traceback.print_last()
            self.logErr("Exception for purchaseId:" + str(purchaseId), sys.exc_info())
            self.conn.rollback()
            raise NameError("Exception for purchaseId:" + str(purchaseId))
        finally:
            cur.close()
