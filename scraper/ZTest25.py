# -*- coding: utf-8 -*-

##############################################################################################################
### TEST - technical test
##############################################################################################################
__author__ = 'omachulskiy'

from scraperPurchase import *
import networkx as nx


class ZTest25:
    def __init__(self):
        self.dbSaver = DBSaver()

    def testNetworkx(self):
        g = nx.Graph()
        cur = self.dbSaver.conn.cursor()
        names = {}
        try:
            cur.execute("SELECT partnerId, inn, p_name, category from tPartner")
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
                g.add_node(row[0], nName=title)
            print "Nodes added:", g.number_of_nodes()
            cur.execute("""
                SELECT partnerId1, partnerId2, title from tPartnerRelation where partnerId2 NOT IN
                        (select partnerId from tPartner where p_name in ('', 'Уставный капитал',
                        'Собственная доля предприятия', 'Учредители не заявлены',
                         'Департамент имущества города Москвы',
                         'Правительство Российской Федерации, Указ Президента РФ от 20 мая 2004г. №649',
                         'Правительство РФ, БУ', 'Департамент имущества города Москвы (государственное учреждение)',
                         'Росимущество, Учреждение', 'Государственная Фельдъегерская Служба Российской Федерации'
                         ) or inn in ('7710723134'))
            """)
            rows = cur.fetchall()
            for row in rows:
                g.add_edge(row[0], row[1], eTitle=row[2])
            print "Edges added:", g.number_of_nodes()

            concomps = nx.connected_components(g)
            biggestComponent = []
            for comp in concomps:
                print "connected_component:", comp
                if len(comp) > len(biggestComponent):
                    biggestComponent = comp

                    # spath = nx.shortest_path(g, 101648, 104707)
                    # for n in spath:
                    #     print "\t", names[n], (g[n])
            print "biggestComponent=", biggestComponent

            theConnNode = None
            numConnections = 0
            for nn in biggestComponent:
                nbrs = nx.neighbors(g, nn)
                print "analyzing node", nn, ", neighbours=", nbrs
                if len(nbrs) > numConnections:
                    theConnNode = nn
                    numConnections = len(nbrs)
                    print "switched to", theConnNode, numConnections
            print "Finalist is ", self.nodeInfo(theConnNode), "neighnours:"
            for nbr in nx.neighbors(g, theConnNode):
                print "\t", self.nodeInfo(nbr)

        finally:
            self.dbSaver.conn.close()

    def nodeInfo(self, partnerId):
        cur = self.dbSaver.conn.cursor()
        cur.execute(
            "SELECT partnerId, inn, p_name, category from tPartner WHERE partnerId=%s",
            [partnerId])
        (ppId, inn, name, category) = cur.fetchone()
        return "[" + str(partnerId) + "/" + str(inn) + "/" + str(name) + "/" + str(
            category) + "]"


ZTest25().testNetworkx()
