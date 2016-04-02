# -*- coding: utf-8 -*-

class ScrapingTask:
    def __init__(self, taskObject, wdf):
        self.taskObject = taskObject
        self.wdf = wdf

    # def exposed_wdf(self):
    #     return self.wdf
    #
    # def exposed_taskObject(self):
    #     return self.taskObject

    def __repr__(self):
        return "<ScrapingTask" + str(self.wdf) + ", " + str(self.taskObject) + ">"


