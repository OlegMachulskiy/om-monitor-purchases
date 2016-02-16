# -*- coding: utf-8 -*-

import datetime


class PurchasesPostETL:
    def __init__(self, conn):
        self.conn = conn

    def runPostETL(self):
        self.runQueriesList0()
        self.parseUnparsedDates()
        self.parseUnparsedNumbers()

    def runQueriesList0(self):
        sqls = [
            """   insert into tPurchaseDetails (purchaseId) 	(select purchaseId from  tPurchase tp	where not exists (select * from tPurchaseDetails  tpd1 where tpd1.purchaseId = tp.purchaseId))
            """
            ,
            """
            update tPurchaseDetails p
            set title = (
                select textValue512
                from tPurchaseRawData pd join tMapping mp
                on pd.keyName=mp.title and mp.tag='purchase_title'
                where pd.purchaseId=p.purchaseId),
            responsible = (
                select textValue512
                from tPurchaseRawData pd join tMapping mp
                on pd.keyName=mp.title and mp.tag='contact_person'
                where pd.purchaseId=p.purchaseId),
            contractAmountT = (
                select textValue512
                from tPurchaseRawData pd join tMapping mp
                on pd.keyName=mp.title and mp.tag='purchase_amount'
                where pd.purchaseId=p.purchaseId),
            customerName = (
                select textValue512
                from tPurchaseRawData pd join tMapping mp
                on pd.keyName=mp.title and mp.tag='purchase_customer'
                where pd.purchaseId=p.purchaseId limit 1),
            stage = (
                select textValue512
                from tPurchaseRawData pd join tMapping mp
                on pd.keyName=mp.title and mp.tag='purchase_stage'
                where pd.purchaseId=p.purchaseId limit 1),
            purchaseType = (
                select textValue512
                from tPurchaseRawData pd join tMapping mp
                on pd.keyName=mp.title and mp.tag='purchase_type'
                where pd.purchaseId=p.purchaseId limit 1)
            """
            ,
            """
            update tPurchaseDetails p  set
            submitStartT = (
                select textValue512
                from tPurchaseRawData pd join tMapping mp
                on pd.keyName like mp.title||'%' and mp.tag='submit_start'
                where pd.purchaseId=p.purchaseId limit 1)
            """
            ,
            """
            update tPurchaseDetails p  set
            submitFinishT = (
                select textValue512
                from tPurchaseRawData pd join tMapping mp
                on pd.keyName like mp.title||'%' and mp.tag='submit_end'
                where pd.purchaseId=p.purchaseId limit 1)
            """
            ,
            """
            update tPurchaseDetails p  set
            requestPublishedT = (
                select textValue512
                from tPurchaseRawData pd join tMapping mp
                on pd.keyName like mp.title||'%' and mp.tag='request_published'
                where pd.purchaseId=p.purchaseId limit 1)
            """
            ,
            u"""
            insert into tPurchaseTags (purchaseId, tagLabel)
            select purchaseId, 'Гагаринский' from tPurchaseDetails pd
            where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
                (lower(title) like '%гагаринск%' OR lower(customername) like '%гагаринск%')
            and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Гагаринский');
                """
            ,
            u"""
            insert into tPurchaseTags (purchaseId, tagLabel)
            select purchaseId, 'ВоробьевыГоры' from tPurchaseDetails pd
            where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
                (lower(title) like '%вороб%' OR lower(customername) like '%вороб%')
            and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='ВоробьевыГоры');
                """
            ,
            u"""
            insert into tPurchaseTags (purchaseId, tagLabel)
            select purchaseId, 'Раменки' from tPurchaseDetails pd
            where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
                (lower(title) like '%рамен%' OR lower(customername) like '%рамен%')
            and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Раменки');
            """
        ]

        cur = self.conn.cursor()
        try:
            for sql in sqls:
                cur.execute(sql)
                print "DONE: " + sql.replace('\n', ' ').replace('\r', '').replace('\t', '') \
                    .replace('    ', ' ').replace('   ', ' ').replace('  ', ' ')
            self.conn.commit()
        finally:
            cur.close()

    def parseUnparsedDates(self):
        cur = self.conn.cursor()
        try:
            cur.execute(
                'select purchaseId, requestPublishedT from tPurchaseDetails where requestPublished is null and requestPublishedT is not null ')
            vals = cur.fetchall()
            for data_row in vals:
                if data_row[1] != None and len(data_row[1]) > 9:
                    parsedDate = datetime.datetime.strptime(data_row[1][:10], "%d.%m.%Y")  # %H:%M:%S
                    cur.execute('update tPurchaseDetails set requestPublished=%s where purchaseId=%s',
                                [parsedDate, data_row[0]])

            cur.execute(
                'select purchaseId, submitStartT from tPurchaseDetails where submitStart is null and submitStartT is not null ')
            vals = cur.fetchall()
            for data_row in vals:
                if data_row[1] != None and len(data_row[1]) > 9:
                    parsedDate = datetime.datetime.strptime(data_row[1][:10], "%d.%m.%Y")  # %H:%M:%S
                    cur.execute('update tPurchaseDetails set submitStart=%s where purchaseId=%s',
                                [parsedDate, data_row[0]])

            cur.execute(
                'select purchaseId, submitFinishT from tPurchaseDetails where submitFinish is null and submitFinishT is not null ')
            vals = cur.fetchall()
            for data_row in vals:
                if data_row[1] != None and len(data_row[1]) > 9:
                    parsedDate = datetime.datetime.strptime(data_row[1][:10], "%d.%m.%Y")  # %H:%M:%S
                    cur.execute('update tPurchaseDetails set submitFinish=%s where purchaseId=%s',
                                [parsedDate, data_row[0]])

            self.conn.commit()
        finally:
            cur.close()

    def parseUnparsedNumbers(self):
        cur = self.conn.cursor()
        try:
            cur.execute(
                'select purchaseId, contractAmountT from tPurchaseDetails where contractAmount is null and contractAmountT is not null ')
            vals = cur.fetchall()
            for data_row in vals:
                if data_row[1] != None and len(data_row[1]) > 1:
                    parsedNum = float(data_row[1].replace(' ', '').replace(',', '.'))
                    cur.execute('update tPurchaseDetails set contractAmount=%s where purchaseId=%s',
                                [parsedNum, data_row[0]])

            self.conn.commit()
        finally:
            cur.close()
