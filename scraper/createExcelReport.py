# -*- coding: utf-8 -*-

from openpyxl import Workbook

from scraperPurchase import *


class CreateExcelReport:
    def __init__(self):
        self.dbs = DBSaver()

    def __del__(self):
        pass

    def writeExcel(self):
        self.dbs.postETL()
        cur = self.dbs.conn.cursor()
        wb = Workbook()

        rc = self.writeGagarinskiySheet(cur, wb)
        print "writeMainSheet: DONE", rc

        for tag in [u'Гагаринский', u'ВоробьевыГоры', u'Университетский', u'Вернадского', u'Ленинский', u'Академический', u'ПрефектураЮЗАО']:
            rc = self.writeTagWinnersSheet(cur, wb,  tag )
            print "writeTagWinnersSheet(", tag ,") : DONE", rc

        # rc = self.writeMoscowWinnersSheet(cur, wb)
        # print "writeMoscowWinnersSheet: DONE", rc
		
        # rc = self.writeAkademicheskiyWinnersSheet(cur, wb)
        # print "writeAkademicheskiyWinnersSheet: DONE", rc
        #
        # rc = self.writePrefekturaUSAOWinnersSheet(cur, wb)
        # print "writePrefekturaUSAOWinnersSheet: DONE", rc

        rc = self.writeErrorsSheet(cur, wb)
        print "writeErrorsSheet: DONE", rc

        # Save the file
        wb.save("purchases.xlsx")
        cur.close()
        print "saved: purchases.xlsx"

    def writeErrorsSheet(self, cur, wb):
        rowCount = 0
        ws = wb.create_sheet()
        ws.title = "Scraping Errors"
        cur.execute("""
SELECT message,
       exc_type,
       exc_value,
       exc_traceback,
       max(loaddate) AS max_date,
       count(1) AS numErrors
FROM tErrorLog
WHERE loadDate > now()- interval '10 days'
GROUP BY message,
         exc_type,
         exc_value,
         exc_traceback
ORDER BY numErrors DESC,
         max_date DESC
		""")
        rows = cur.fetchall()
        ws.append([desc[0] for desc in cur.description])
        for row in rows:
            # Rows can also be appended
            ws.append(row)
            rowCount += 1

        ws.auto_filter.ref = "A:Z"
        ws.auto_filter.add_filter_column(0, ['Fatal*'], False)
        return rowCount

    def writeGagarinskiySheet(self, cur, wb):
        rowCount = 0
        ws = wb.active  # create_sheet()
        ws.title = "Gagarinskiy"
        cur.execute("""
SELECT pp.purchaseId,
       orderId,
       customerName,
       title,
       purchaseType,
       stage ,
       contractAmount,
       _url,
       to_char( coalesce(submitFinish, submitStart, requestPublished), 'YYYY-mm') as SomeDate,
       _loaddate,
       requestPublished,
       submitStart,
       submitFinish,
       responsible,
       contractAmountT,
       requestPublishedT,
       submitStartT,
       submitFinishT
FROM tPurchase pp
JOIN tPurchaseDetails ppd ON pp.purchaseId = ppd.purchaseId
WHERE ppd.title IS NOT NULL
and ppd.purchaseId in (select purchaseId from tPurchaseTags WHERE tagLabel in ('Гагаринский', 'ВоробьевыГоры', 'Университетский'))
		""")
        # select * from vArtList order by loadDate desc
        rows = cur.fetchall()
        ws.append([desc[0] for desc in cur.description])
        for row in rows:
            # Rows can also be appended
            ws.append(row)
            rowCount += 1
        ws.auto_filter.ref = "A:Z"
        return rowCount

    def writeTagWinnersSheet(self, cur, wb, tagName):
        rowCount = 0
        ws = wb.create_sheet()
        ws.title = tagName
        cur.execute("""
SELECT
       ppd.customerName,
       title,
       winnerName,
       winnerINN,
       purchaseType,
       stage ,
       contractAmount as Tender_Amount,
       price as Contract_Price,
       priceT,
       _url,
       to_char( coalesce(submitFinish, submitStart, requestPublished), 'YYYY-mm') as SomeDate,
       contractStatus,
       pp._loaddate,
       requestPublished,
       submitStart,
       submitFinish,
       responsible,
       pp.purchaseId,
       orderId
FROM tPurchase pp
JOIN tPurchaseDetails ppd ON pp.purchaseId = ppd.purchaseId
LEFT JOIN tPurchaseContracts pcc on  pp.purchaseId = pcc.purchaseId
WHERE ppd.title IS NOT NULL
and ppd.purchaseId in (select purchaseId from tPurchaseTags WHERE tagLabel in (%s))
		""", [tagName])
        rows = cur.fetchall()
        ws.append([desc[0] for desc in cur.description])
        for row in rows:
            # Rows can also be appended
            ws.append(row)
            rowCount += 1

        ws.auto_filter.ref = "A:Z"
        # ws.auto_filter.add_filter_column(0, ['Fatal*'], False)
        return rowCount


    def writeMoscowWinnersSheet(self, cur, wb):
        rowCount = 0
        ws = wb.create_sheet()
        ws.title = "Moscow Winners"
        cur.execute("""
SELECT
       ppd.customerName,
       title,
       winnerName,
       purchaseType,
       stage ,
       contractAmount as Tender_Amount,
       price as Contract_Price,
       _url,
       to_char( coalesce(submitFinish, submitStart, requestPublished), 'YYYY-mm') as SomeDate,
       pp._loaddate,
       requestPublished,
       submitStart,
       submitFinish,
       responsible,
       pp.purchaseId,
       orderId,
       priceT as Contract_Price_Text
FROM tPurchase pp
JOIN tPurchaseDetails ppd ON pp.purchaseId = ppd.purchaseId
LEFT JOIN tPurchaseContracts pcc on  pp.purchaseId = pcc.purchaseId
WHERE lower(ppd.title) like '%москв%' OR lower(ppd.customerName) like '%москв%'

		""")
        rows = cur.fetchall()
        ws.append([desc[0] for desc in cur.description])
        for row in rows:
            # Rows can also be appended
            ws.append(row)
            rowCount += 1

        ws.auto_filter.ref = "A:Z"
        # ws.auto_filter.add_filter_column(0, ['Fatal*'], False)
        return rowCount


a = CreateExcelReport()
a.writeExcel()
