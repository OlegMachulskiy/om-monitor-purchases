# -*- coding: utf-8 -*-

import json
import pickle

from ScrapingQueue import ScrapingQueue
from rpyc.utils.server import ThreadedServer
import rpyc
from DBSaver import DBSaver


class ScrapingHub(rpyc.Service):
    """
    Scraping HUB.
    """

    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        print "on_connect:", self
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        print "on_disconnect:", self
        pass

    # def get_service_name(self):
    #     return self.__class__

    def exposed_getNextTask(self):  # this is an exposed method
        print "method enter: exposed_getNextTask"
        rv = ScrapingQueue().getNextTask()
        print "method result: exposed_getNextTask", rv
        return pickle.dumps(rv.__dict__)

    def exposed_markTaskCompleted(self, ssid):  # this is an exposed method
        print "method enter: exposed_markTaskCompleted", ssid
        ScrapingQueue().markTaskCompleted(ssid)

    def exposed_connection(self):  # this is an exposed method
        print "method enter: exposed_connection"
        dbSaver = DBSaver()
        return str(dbSaver.conn)


if __name__ == "__main__":
    t = ThreadedServer(ScrapingHub, port=51715)
    # protocol_config={"allow_public_attrs": True})

    t.start()
