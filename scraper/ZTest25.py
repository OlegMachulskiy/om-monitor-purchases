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
                g.add_node(row[0], title=title)
            print "Nodes added:", g.number_of_nodes()
            cur.execute("""
                SELECT partnerId1, partnerId2, title from tPartnerRelation where partnerId2 NOT IN
                        (select partnerId from tPartner where p_name in ('', 'Уставный капитал', 'Собственная доля предприятия', 'Учредители не заявлены'))
            """)
            rows = cur.fetchall()
            for row in rows:
                g.add_edge(row[0], row[1], title=row[2])
            print "Edges added:", g.number_of_nodes()

            concomps = nx.connected_components(g)
            for comp in concomps:
                print "connected_component:", comp
                if len(comp)>10:
                    for nds in comp:
                        if len(g[nds])>5:
                            print len(g[nds]), g[nds]

            spath = nx.shortest_path(g, 101648, 104707)
            for n in spath:
                print "\t", (g[n])

        finally:
            self.dbSaver.conn.close()


ZTest25().testNetworkx()
