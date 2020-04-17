#! /usr/bin/env python
# -*- coding: utf-8 -*-

def logAnalyzer(name, name2):

    moreInfo_yes = 0  # moreInfo,0,yes              # no considerare se secondo elemento è 2
    moreInfo_no = 0  # moreInfo,0,no
    moreInfo_keyword = 0  # moreInfo,0,keyword
    sectionChosen_anothersection = 0  # presentSection,section chosen,another section
    anotherSections_yes = 0  # presentSection,another section,yes
    anotherSections_no = 0  # presentSection,another section,no
    anotherTopic_yes = 0  # anotherTopic,yes
    anotherTopic_no = 0  # anotherTopic,no
    anotherTopic_keyword_true = 0  # anotherTopic,keyword,true
    anotherTopic_keyword_false = 0  # anotherTopic,keyword,false
    topic_emptylist = 0  # topicProposer,empty list

    f = open(name, "r")
    if f.mode == 'r':
        txt = f.read()

    rows = txt.split("\n")

    for x in range(len(rows)):
        elements = rows[x].split(",")
        if elements[0] == "moreInfo":
                if elements[1] != 2:
                    if elements[2] == "yes":
                        moreInfo_yes +=1
                    elif elements[2] == "no":
                        moreInfo_no +=1
                    elif elements[2] == "keyword":
                        moreInfo_keyword +=1
        if elements[0] == "presentSection":
            if elements[1] == "section chosen":
                if elements[2] == "another section":
                    sectionChosen_anothersection +=1
        if elements[0] == "presentSection":
            if elements[1] == "another section":
                if elements[2] == "yes":
                    anotherSections_yes +=1
                elif elements[2] == "no":
                    anotherSections_no +=1
        if elements[0] == "anotherTopic":
            if elements[1] == "yes":
                anotherTopic_yes +=1
            elif elements[1] == "no":
                anotherTopic_no +=1
        if elements[0] == "anotherTopic":
            if elements[1] == "keyword":
                if elements[2] == "true":
                    anotherTopic_keyword_true +=1
                elif elements[2] == "false":
                    anotherTopic_keyword_false +=1
        if elements[0] == "topicProposer":
            if elements[1] == "empty list":
                topic_emptylist +=1

    f.close()

    f = open(name2, "a+")
    f.write("moreInfo_yes: " + str(moreInfo_yes) + "\n")
    f.write("moreInfo_no: " + str(moreInfo_no) + "\n")
    f.write("moreInfo_keyword: " + str(moreInfo_keyword) + "\n")
    f.write("sectionChosen_anothersection: " + str(sectionChosen_anothersection) + "\n")
    f.write("anotherSections_yes: " + str(anotherSections_yes) + "\n")
    f.write("anotherSections_no: " + str(anotherSections_no) + "\n")
    f.write("anotherTopic_no: " + str(anotherTopic_no) + "\n")
    f.write("anotherTopic_keyword_true: " + str(anotherTopic_keyword_true) + "\n")
    f.write("anotherTopic_keyword_false: " + str(anotherTopic_keyword_false) + "\n")
    f.write("topic_emptylist: " + str(topic_emptylist) + "\n")
    f.close()