# -*- coding: utf-8 -*-
import os.path

from ScrapingQueue import *
# from ScrapingGrid import *
import time
import sys
import traceback
import threading


class ScrapingNode(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.q = ScrapingQueue()
        self.dbSaver = DBSaver()

    def __del__(self):
        del self.dbSaver

    def run(self):
        scrapingTask = None
        scrapingTaskKey = None

        proxyAddr = None
        current_milli_time = int(round(time.time() * 1000))
        try:

            doRun = True

            while doRun:
                if os.path.isfile("STOP"):
                    print "STOP file found. Quitting..."
                    break
                scrapingTask = self.q.getNextTask()
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

                    scrapingTask.wdf.runScrapingForEntity(self.dbSaver, scraper,
                                                          scrapingTask.taskObject)

                    if scrapingTask.wdf.collectProxyStats():
                        self.dbSaver.storeHTTPProxyResult(proxyAddr,
                                                          int(round(
                                                              time.time() * 1000)) - current_milli_time,
                                                          "Success")
                finally:
                    if scraper != None:
                        del scraper
                    if scrapingTask is not None:
                        self.q.markTaskCompleted(scrapingTaskKey)

        except Exception as ex:
            traceback.print_exc()
            if scrapingTask.wdf.collectProxyStats():
                self.dbSaver.storeHTTPProxyResult(proxyAddr, int(
                    round(time.time() * 1000)) - current_milli_time, str(ex) + ":" + scrapingTaskKey)
            self.dbSaver.logErr("Failure:" + scrapingTaskKey, sys.exc_info())
            raise ex
        finally:
            pass
            # if dbSaver != None:
            #     del dbSaver


def startScrapingNode(threadCount=7):
    sNode = ScrapingNode()
    sNode.start()

    while True:
        if os.path.isfile("STOP"):
            print "STOP file found. Quitting..."
            break
        time.sleep(3)
        print "Active threads:", threading.active_count(), \
            "qLength:", ScrapingQueue().getLength(), \
            "pregress=", ScrapingQueue().getProgress(), \
            "currentThread=", threading.current_thread, \
            ""
        # for th in threading.enumerate():
        #     print(th)
        #     traceback.print_stack(sys._current_frames()[th.ident])
        #     print()

        if threading.active_count() < threadCount:
            print "Start new node"
            sNode = ScrapingNode()
            sNode.start()


if __name__ == "__main__":
    startScrapingNode(threadCount=12)  # TODO - parse command line parameters
