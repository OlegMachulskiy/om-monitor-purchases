# -*- coding: utf-8 -*-
import random

# import rpyc
import threading


# class ScrapingHub:
#     """
#     Scraping HUB.
#     """
#
#     def on_connect(self):
#         # code that runs when a connection is created
#         # (to init the serivce, if needed)
#         print "on_connect:", self
#         self.dbSaver = DBSaver()
#         pass
#
#     def on_disconnect(self):
#         # code that runs when the connection has already closed
#         # (to finalize the service, if needed)
#         print "on_disconnect:", self
#         del self.dbSaver
#         pass
#
#     def exposed_getNextTask(self):  # this is an exposed method
#         print "method enter: exposed_getNextTask"
#         sq = ScrapingQueue()
#         rv = sq.getNextTask()
#         print "method result: exposed_getNextTask", rv
#         return rv
#
#     def exposed_markTaskCompleted(self, ssid):  # this is an exposed method
#         print "method enter: exposed_getNextTask", ssid
#         sq = ScrapingQueue()
#         sq.markTaskCompleted(ssid)
#
#     def exposed_getDBSaver(self):
#         return self.dbSaver
#
#         # def exposed_storeHTTPProxyResul(self):
#
#
# if __name__ == "__main__":
#     from rpyc.utils.server import ThreadedServer
#
#     t = ThreadedServer(ScrapingHub, port=51715, protocol_config={"allow_public_attrs": True})
#
#     t.start()
