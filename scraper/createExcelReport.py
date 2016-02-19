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
        rc = self.writeMainSheet(cur, wb)
        print "writeMainSheet: DONE", rc
        rc = self.writeLocalWinnersSheet(cur, wb)
        print "writeLocalWinnersSheet: DONE", rc
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

    def writeMainSheet(self, cur, wb):
        rowCount = 0
        ws = wb.active  # create_sheet()
        ws.title = "Tenders"
        cur.execute("""
SELECT pp.purchaseId,
       orderId,
       customerName,
       title,
       purchaseType,
       stage ,
       contractAmount,
       _url,
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

    def writeLocalWinnersSheet(self, cur, wb):
        rowCount = 0
        ws = wb.create_sheet()
        ws.title = "Local Winners"
        cur.execute("""
SELECT
       ppd.customerName,
       title,
       winnerName,
       purchaseType,
       stage ,
       contractAmount as Tender_Amount,
       price as Contract_Price,
       priceT,
       _url,
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
and ppd.purchaseId in (select purchaseId from tPurchaseTags WHERE tagLabel in ('Гагаринский', 'ВоробьевыГоры', 'Университетский'))
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


a = CreateExcelReport()

a.writeExcel()
