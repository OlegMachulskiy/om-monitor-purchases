# -*- coding: utf-8 -*-

import datetime
import traceback


class PurchasesPostETL:
    sql_PD_1 = """
        update tPurchaseDetails p
        set title = (
            select textValue512
            from tPurchaseRawData pd WHERE pd.keyName in ('Наименование закупки', 'Наименование объекта закупки')
            AND pd.purchaseId=p.purchaseId
            limit 1)
		"""
    sql_PD_2 = """
        update tPurchaseDetails p
        SET responsible = (
            select textValue512
            from tPurchaseRawData pd join tMapping mp
            on pd.keyName=mp.title and mp.tag='contact_person'
            where pd.purchaseId=p.purchaseId
            limit 1)
		"""
    sql_PD_3 = """
        update tPurchaseDetails p
        SET contractAmountT = (
            select textValue512
            from tPurchaseRawData pd join tMapping mp
            on pd.keyName=mp.title and mp.tag='purchase_amount'
            where pd.purchaseId=p.purchaseId
            limit 1)
		"""
    sql_PD_4 = """
        update tPurchaseDetails p
        SET customerName = (
            select textValue512
            from tPurchaseRawData pd join tMapping mp
            on pd.keyName=mp.title and mp.tag='purchase_customer'
            where pd.purchaseId=p.purchaseId
            limit 1)
		"""
    sql_PD_5 = """
        update tPurchaseDetails p
        SET stage = (
            select textValue512
            from tPurchaseRawData pd join tMapping mp
            on pd.keyName=mp.title and mp.tag='purchase_stage'
            where pd.purchaseId=p.purchaseId
            limit 1)
		"""
    sql_PD_6 = """
        update tPurchaseDetails p
        SET purchaseType = (
            select textValue512
            from tPurchaseRawData pd join tMapping mp
            on pd.keyName=mp.title and mp.tag='purchase_type'
            where pd.purchaseId=p.purchaseId
            limit 1)
        """
    sql_PD_7 = """
        update tPurchaseDetails p  set
        submitStartT = (
            select textValue512
            from tPurchaseRawData pd join tMapping mp
            on pd.keyName like mp.title||'%' and mp.tag='submit_start'
            where pd.purchaseId=p.purchaseId
            limit 1)
        """
    sql_PD_8 = """
        update tPurchaseDetails p  set
        submitFinishT = (
            select textValue512
            from tPurchaseRawData pd join tMapping mp
            on pd.keyName like mp.title||'%' and mp.tag='submit_end'
            where pd.purchaseId=p.purchaseId
            limit 1)
        """
    sql_PD_9 = """
        update tPurchaseDetails p  set
        requestPublishedT = (
            select textValue512
            from tPurchaseRawData pd join tMapping mp
            on pd.keyName like mp.title||'%' and mp.tag='request_published'
            where pd.purchaseId=p.purchaseId
            limit 1)
        """
    sqls0 = [
        """
        insert into tPurchaseDetails (purchaseId) 	(select purchaseId from  tPurchase tp	where not exists (select * from tPurchaseDetails  tpd1 where tpd1.purchaseId = tp.purchaseId))
        """
        ,
        sql_PD_1, sql_PD_2, sql_PD_3, sql_PD_4, sql_PD_5, sql_PD_6, sql_PD_7, sql_PD_8, sql_PD_9,
        """
        insert into tPurchaseTags (purchaseId, tagLabel)
        select purchaseId, 'Гагаринский' from tPurchaseDetails pd
        where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
            (lower(title) like '%гагаринск%' OR lower(customername) like '%гагаринск%')
        and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Гагаринский');
            """
        ,
        """
        insert into tPurchaseTags (purchaseId, tagLabel)
        select purchaseId, 'ВоробьевыГоры' from tPurchaseDetails pd
        where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
            (lower(title) like '%вороб%' OR lower(customername) like '%вороб%')
        and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='ВоробьевыГоры');
            """
        ,
        """
        insert into tPurchaseTags (purchaseId, tagLabel)
        select purchaseId, 'Раменки' from tPurchaseDetails pd
        where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
            (lower(title) like '%рамен%' OR lower(customername) like '%рамен%')
        and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Раменки');
        """
        ,
        """
        insert into tPurchaseTags (purchaseId, tagLabel)
        select purchaseId, 'Самара' from tPurchaseDetails pd
        where (lower(title) like '%самар%' OR lower(customername) like '%самар%')
        and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Самара');
        """
        ,
        """
        insert into tPurchaseTags (purchaseId, tagLabel)
        select purchaseId, 'Университетский' from tPurchaseDetails pd
        where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
        (lower(title) like '%университетск%' OR lower(customername) like '%университетск%') AND
        (lower(title) like '%просп%' OR lower(customername) like '%просп%')
        and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Университетский');
        """
        ,
        """
        insert into tPurchaseTags (purchaseId, tagLabel)
        select purchaseId, 'Вернадского' from tPurchaseDetails pd
        where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
        (lower(title) like '%вернадского%' OR lower(customername) like '%вернадского%') AND
        (lower(title) like '%просп%' OR lower(customername) like '%просп%')
        and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Вернадского');
        """
        ,
        """
        insert into tPurchaseTags (purchaseId, tagLabel)
        select purchaseId, 'Вавилова' from tPurchaseDetails pd
        where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
        (lower(title) like '%вавилов%' OR lower(customername) like '%вавилов%')
        and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Вавилова');
        """
        ,
        """
        insert into tPurchaseTags (purchaseId, tagLabel)
        select purchaseId, 'Ленинский' from tPurchaseDetails pd
        where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
        (lower(title) like '%ленинск%' OR lower(customername) like '%ленинск%') AND
        (lower(title) like '%просп%' OR lower(customername) like '%просп%')
        and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Ленинский');
        """
        ,
        """
        insert into tPurchaseTags (purchaseId, tagLabel)
        select purchaseId, 'Академический' from tPurchaseDetails pd
        where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
        (lower(title) like '%академическ%' OR lower(customername) like '%академическ%')
        and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Академический');
        """
        ,
        """
        insert into tPurchaseTags (purchaseId, tagLabel)
        select purchaseId, 'ПрефектураЮЗАО' from tPurchaseDetails pd
        where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
        (lower(title) like '%префект%' OR lower(customername) like '%префект%') AND
        (lower(title) like '%юзао%' OR lower(customername) like '%юзао%' OR lower(title) like '%юго%' OR lower(customername) like '%юго%')
        and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='ПрефектураЮЗАО');
        """
        ,
        """
        insert into tPurchaseTags (purchaseId, tagLabel)
        select purchaseId, 'Благоустройство' from tPurchaseDetails pd
        where (lower(title) like '%москв%' OR lower(customername) like '%москв%') AND
        (lower(title) like '%благоустройст%' OR lower(customername) like '%благоустройст%'
        OR lower(title) like '%реконструкци%' OR lower(customername) like '%реконструкци%'
        OR lower(title) like '%эколог%' OR lower(customername) like '%эколог%'
        OR lower(title) like '%озелен%' OR lower(customername) like '%озелен%'
		OR lower(title) like '%противогололедн%' OR lower(title) like '%противогололедн%'
		OR lower(title) like '%вырубк%' OR lower(title) like '%покос%'
		OR lower(title) like '%газон%' OR lower(title) like '%кустарни%' )
        and not exists (select 1 from tPurchaseTags ptg where pd.purchaseId=ptg.purchaseId and ptg.tagLabel='Благоустройство');
        """
    ]

    sqls1 = [
        """
        update tPurchaseContracts p
        set winnerINN = (
            select textValue512
            from tContractRawData crd join tMapping mp
            on crd.purchaseContractId=p.purchaseContractId and keyName='participantInfoTable:ИНН:' limit 1)
        where winnerINN  is null
        """
        ,
        """
        update tPurchaseContracts p
        set contractStatus = (
            select textValue512
            from tContractRawData crd join tMapping mp
            on crd.purchaseContractId=p.purchaseContractId and keyName='"Статус контракта"' limit 1)
        """
        ,
        """
        insert into tPartner (partnerId, inn, category)
        (select nextval('idGen'), winnerINN, 'O' from  (select distinct winnerINN from tPurchaseContracts) tpc
        where not exists (select * from tPartner  tpd1 where tpd1.inn = tpc.winnerINN) and winnerINN is not null)
        """
        ,
        """insert into tPartner (partnerId, inn, category)
           (select nextval('idGen'), inn, 'O' from  (select distinct textValue512 as inn
               from tPurchaseBidRawData tbrd join tPurchaseBid tb ON tbrd.bidId=tb.bidId
               WHERE keyName='ИНН') tpc
           WHERE not exists (select * from tPartner  tpd1 where tpd1.inn = tpc.inn) and inn is not null)
            """
        ,
        """ UPDATE tPurchaseBid ubd SET partnerId=
            (select distinct tp.partnerId
            from tPurchaseBidRawData tbrd
            join tPurchaseBid tb ON tbrd.bidId=tb.bidId AND keyName='ИНН'
            JOIN tPartner tp ON tp.inn = tbrd.textValue512
                        and tb.bidId=ubd.bidId
                LIMIT 1)  """

        ,
        """
        insert into tOrganization (partnerId)
        SELECT partnerId from  tPartner tpc where category='O' AND not exists (select * from tOrganization  tpd1 where tpd1.partnerId = tpc.partnerId)
        """

    ]

    def __init__(self, conn):
        self.conn = conn

    def runPostETL_for_Purchase(self, purchase):
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO tPurchaseDetails (purchaseId) 	"
                        " (SELECT purchaseId from  tPurchase tp	"
                        " WHERE not exists (select * from tPurchaseDetails  tpd1 WHERE tpd1.purchaseId = tp.purchaseId)"
                        " AND tp.purchaseId=%s)", [purchase.purchaseId])
            for qq in [self.sql_PD_1, self.sql_PD_2, self.sql_PD_3, self.sql_PD_4, self.sql_PD_5, self.sql_PD_6]:
                sql = qq + " WHERE purchaseId=%s"
                cur.execute(sql, [purchase.purchaseId])
                print "DONE: ", self.normalizeSpaces(sql), [purchase.purchaseId]

            self.conn.commit()
        finally:
            cur.close()

    def runPostETL(self):
        self.runQueriesList0(self.sqls0)
        self.runQueriesList0(self.sqls1)
        self.parseUnparsedDates()
        self.parsePurchaseDetailNumbers()
        self.parsePurchaseContractsNumbers()

    def runQueriesList0(self, sqls):
        cur = self.conn.cursor()
        try:
            for sql in sqls:
                cur.execute(sql)
                print "DONE: " + self.normalizeSpaces(sql)
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
            print "DONE:parseUnparsedDates"

    def parsePurchaseDetailNumbers(self):
        cur = self.conn.cursor()
        try:
            cur.execute(
                'select purchaseId, contractAmountT from tPurchaseDetails where contractAmount is null and contractAmountT is not null ')
            vals = cur.fetchall()
            for data_row in vals:
                if data_row[1] != None and len(data_row[1]) > 1:
                    parsedNum = 0
                    try:
                        parsedNum = float(data_row[1].replace(' ', '').replace(',', '.'))
                    except Exception as ex:
                        print "parsePurchaseDetailNumbers:failure for ", data_row[1]
                        # traceback.print_tb(ex)
                    cur.execute('update tPurchaseDetails set contractAmount=%s where purchaseId=%s',
                                [parsedNum, data_row[0]])

            self.conn.commit()
        finally:
            cur.close()
            print "DONE:parsePurchaseDetailNumbers"

    def parsePurchaseContractsNumbers(self):
        cur = self.conn.cursor()
        try:
            cur.execute(
                'select purchaseContractId, priceT from tPurchaseContracts where (price is null or price<=0) and priceT is not null ')
            vals = cur.fetchall()
            for data_row in vals:
                if data_row[1] != None and len(data_row[1]) > 1:
                    parsedNum = -1
                    try:
                        parsedNum = float(
                            data_row[1].replace(' Российский рубль', '').replace(' ', '').replace(',', '.'))
                    except Exception as ex:
                        print "parsePurchaseContractsNumbers:failure for ", data_row[1]
                        # traceback.print_tb(ex)
                    cur.execute('update tPurchaseContracts set price=%s where purchaseContractId=%s',
                                [parsedNum, data_row[0]])

            self.conn.commit()
        finally:
            cur.close()
            print "DONE:parsePurchaseContractsNumbers"

    def normalizeSpaces(self, sql):
        return sql.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ') \
                    .replace('     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ')