# -*- coding: utf-8 -*-
import random

import pickle
import rpyc

c = rpyc.connect("localhost", 51715)

for i in range(1, 23):
    pkl = c.root.getNextTask()
    # print pkl
    nextTask = pickle.loads(pkl)
    siid = nextTask['wdf'].getSIID(nextTask['taskObject'])
    print siid, nextTask
    c.root.markTaskCompleted(siid)