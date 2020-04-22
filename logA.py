#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
from logAnalyzer import logAnalyzer

timeStamp = time.time()
name =  "log/GroupA-T/log" + str(timeStamp) + ".txt"
name2 = "log/GroupA-T/res" + str(timeStamp) + ".txt"
f = open(name, "a+")

def log(text):
    f.write(text + "\n")

def closeLog():
    f.close()
    logAnalyzer(name, name2)