# -*- coding: utf-8 -*-

##############################################################################################################
### TEST - technical test  NetworkX library
##############################################################################################################
import math

__author__ = 'omachulskiy'

from scraperPurchase import *
import networkx as nx


class ZTest25:
    def __init__(self):
        self.dbSaver = DBSaver()
        # self.dbSaver.postETL()

    def testNetworkx(self):
        g = nx.Graph()
        cur = self.dbSaver.conn.cursor()
        names = {}
        try:
            mapOfOurNodes = self.loadSetOfOurNodes()

            cur.execute("SELECT partnerId, inn, p_name, category FROM tPartner")
            rows = cur.fetchall()
            for row in rows:
                title = "("
                if row[1] != None: title += row[1]
                title += '/'
                if row[2] != None: title += row[2]
                title += '/'
                if row[3] != None: title += row[3]
                title += ')'
                names[row[0]] = title
                vIsKeyNode = (int(row[0]) in mapOfOurNodes)
                vNodetype = row[3]
                if vNodetype is None:
                    vNodetype = "partner"
                g.add_node(int(row[0]), pp_Title=title.decode("utf-8"), pp_isKeyNode=vIsKeyNode, pp_nodeType=vNodetype)
            print "Nodes added:", g.number_of_nodes()

            cur.execute("""
                SELECT partnerId1, partnerId2, title from tPartnerRelation where partnerId2 NOT IN
                        (select partnerId from tPartner where p_name in ('', 'Уставный капитал',
                        'Собственная доля предприятия', 'Учредители не заявлены',
                         'Государственная Фельдъегерская Служба Российской Федерации',
                         'Департамент имущества города Москвы',
                         'Правительство Российской Федерации, Указ Президента РФ от 20 мая 2004г. №649',
                         'Правительство РФ, БУ', 'Департамент имущества города Москвы (государственное учреждение)',
                         'Росимущество, Учреждение', 'Лица имеющие вид на жительство (1)'
                         ) or inn in ('7710723134'))
            """)
            rows = cur.fetchall()
            for row in rows:
                vTitle = row[2]
                if vTitle is None:
                    vTitle = "undefined"
                g.add_edge(int(row[0]), int(row[1]), pp_Title=vTitle.decode("utf-8"), pp_edgeType="SBIS")
            print "Edges added:", g.number_of_nodes()

            self.appendGagarinskiyAndPurchasesToGraph(g)

            nx.write_graphml(g, "partners.graphml", encoding="utf-8")

        finally:
            self.dbSaver.conn.close()

    def nodeInfo(self, partnerId):
        cur = self.dbSaver.conn.cursor()
        cur.execute(
            "SELECT partnerId, inn, p_name, category FROM tPartner WHERE partnerId=%s",
            [partnerId])
        (ppId, inn, name, category) = cur.fetchone()
        return "[" + str(partnerId) + "/" + str(inn) + "/" + str(name) + "/" + str(
            category) + "]"

    def loadSetOfOurNodes(self):
        cur = self.dbSaver.conn.cursor()
        cur.execute(
            """

select partnerId from tPartner where inn in (
select distinct winnerINN from tPurchaseTags tpt
join tPurchaseDetails  tpd  on tpd.purchaseId=tpt.purchaseId
left join tPurchaseContracts tpc on tpc.purchaseId=tpd.purchaseId
where tpt.tagLabel in ('Гагаринский')
and winnerINN is not null
)

            """)
        # , 'ВоробьевыГоры','Академический','ПрефектураЮЗАО' /*,'Вернадского','Университетский','Раменки','Ленинский'*/
        rv = set([])
        rows = cur.fetchall()
        for row in rows:
            rv.add(int(row[0]))
        return rv

    def appendGagarinskiyAndPurchasesToGraph(self, g):
        cur = self.dbSaver.conn.cursor()

        cur.execute("""

SELECT
       ppd.customerName,
       pp.purchaseId,
       title,
       winnerINN,
       _url,
       ppd.contractAmount,
       tp.partnerId
FROM tPurchase pp
JOIN tPurchaseDetails ppd ON pp.purchaseId = ppd.purchaseId
LEFT JOIN tPurchaseContracts pcc on  pp.purchaseId = pcc.purchaseId
LEFT JOIN tPartner tp on tp.inn =  pcc.winnerInn
WHERE ppd.title IS NOT NULL
and ppd.purchaseId in (select purchaseId from tPurchaseTags WHERE tagLabel in ('Гагаринский'))

            """)
        rows = cur.fetchall()
        cnt = 0
        for row in rows:
            customerTitle = row[0].decode("utf-8")
            if customerTitle is None or row[1] is None:
                continue
            g.add_node(customerTitle, pp_nodeType="Customer", pp_Title=customerTitle)
            vPurchaseTitle = row[2].decode("utf-8")
            contractAmount = row[5]
            if contractAmount is None:
                contractAmount = 10
            contractSize = round(math.log10(float(contractAmount)), 0)
            g.add_node(int(row[1]), pp_nodeType="Purchase", pp_Title=vPurchaseTitle, pp_Size=contractSize,
                       pp_contractAmount=float(contractAmount))
            g.add_edge(customerTitle, int(row[1]), pp_edgeType="customer2purchase")
            cnt += 1
            if row[6] is not None:
                g.add_edge(int(row[1]), int(row[6]), pp_edgeType="purchase2winner")
        print "Added purchases", cnt


ZTest25().testNetworkx()
