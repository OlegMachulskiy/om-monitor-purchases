import psycopg2
from openpyxl import Workbook


class CreateExcelReport:
    def __init__(self):
        self.conn = psycopg2.connect("dbname='MonitorPurchase' user='postgres' host='localhost' password='q1w2e3r4'")

    def __del__(self):
        pass

    def updateData(self):
        cur = self.conn.cursor()
        cur.execute("""
         insert into tPurchaseDetails (purchaseId)
	(select purchaseId from  tPurchase tp
	where not exists (select * from tPurchaseDetails  tpd1 where tpd1.purchaseId = tp.purchaseId))
        """)
        cur.execute("""

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
;
        """)

        self.conn.commit()
        cur.close()

    def writeExcel(self):
        cur = self.conn.cursor()
        wb = Workbook()
        rc = self.writeMainSheet(cur, wb)
        print "writeMainSheet: DONE", rc
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
        ws.title = "Articles"
        cur.execute("""
        select * from vPurchases
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


a = CreateExcelReport()
a.updateData()
a.writeExcel()
