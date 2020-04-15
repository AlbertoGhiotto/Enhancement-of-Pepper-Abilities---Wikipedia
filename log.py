#! /usr/bin/env python

import time

name = ""
f = open(name, "a+")  # a+:append

def initLog():
    timeStamp = time.asctime()
    name = "log" + timeStamp + ".txt"
    f = open(name, "a+")  # a+:append

def log(text):
    f.write(text + "\n")

def closeLog():
    f.close()