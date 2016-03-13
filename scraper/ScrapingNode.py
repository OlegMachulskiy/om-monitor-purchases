# -*- coding: utf-8 -*-

from ScrapingGrid import *
import rpyc
import time
import sys
import traceback


class ScrapingNode(threading.Thread):
    def __init__(self, serverIP, port):
        threading.Thread.__init__(self)
        self.rpyConnect = rpyc.connect(serverIP, port, config={"allow_public_attrs": True})

    def run(self):
        scrapingTask = None
        scrapingTaskKey = None

        proxyAddr = None
        current_milli_time = int(round(time.time() * 1000))
        try:

            doRun = True

            while doRun:
                scrapingTask = self.rpyConnect.root.getNextTask()
                print "Got scraping task:", scrapingTask
                scrapingTaskKey = scrapingTask.wdf.getSIID(scrapingTask.taskObject)

                current_milli_time = int(round(time.time() * 1000))
                if scrapingTask is None:
                    time.sleep(20)
                    doRun = False
                    break

                scraper = None
                try:
                    scraper = ScrapZakupkiGovRu()
                    proxyAddr = scraper.initializeWebdriver(useProxy=scrapingTask.wdf.useProxy(),
                                                            defaultHttpTimeout=scrapingTask.wdf.defaultHttpTimeout())

                    scrapingTask.wdf.runScrapingForEntity(self.rpyConnect.root.getDBSaver(), scraper,
                                                          scrapingTask.taskObject)

                    if scrapingTask.wdf.collectProxyStats():
                        self.rpyConnect.root.getDBSaver().storeHTTPProxyResult(proxyAddr,
                                                                  int(round(
                                                                      time.time() * 1000)) - current_milli_time,
                                                                  "Success")
                finally:
                    if scraper != None:
                        del scraper
                    if scrapingTask is not None:
                        self.rpyConnect.root.markTaskCompleted(scrapingTaskKey)

        except Exception as ex:
            traceback.print_exc()
            if scrapingTask.wdf.collectProxyStats():
                self.rpyConnect.root.getDBSaver().storeHTTPProxyResult(proxyAddr, int(
                    round(time.time() * 1000)) - current_milli_time, str(ex) + ":" + scrapingTaskKey)
            self.rpyConnect.root.getDBSaver().logErr("Failure:" + scrapingTaskKey, sys.exc_info())
            raise ex
        finally:
            pass
            # if dbSaver != None:
            #     del dbSaver


def startScrapingNode(srv_ip="192.168.1.12", port=51715, threadCount=7):
    sNode = ScrapingNode(srv_ip, port)
    sNode.start()

    while True:
        time.sleep(3)
        print "Active threads:", threading.active_count(), \
            "currentThread:", threading.current_thread
        # "Queue length:", len(vgScrapingEntities), \
        # "In Progress:", vgEntitiesInProgress

        # for th in threading.enumerate():
        #     print(th)
        #     traceback.print_stack(sys._current_frames()[th.ident])
        #     print()

        if threading.active_count() < threadCount:
            print "Start new node"
            sNode = ScrapingNode(srv_ip, port)
            sNode.start()


if __name__ == "__main__":
    startScrapingNode(threadCount=7)  # TODO - parse command line parameters
