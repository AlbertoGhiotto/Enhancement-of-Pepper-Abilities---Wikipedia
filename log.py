#! /usr/bin/env python

import time

timeStamp = time.time()
name = "log/log" + str(timeStamp) + ".txt"
f = open(name, "a+")

def log(text):
    f.write(text + "\n")

def closeLog():
    f.close()