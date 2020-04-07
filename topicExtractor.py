#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import meaningcloud


# @param model str - Name of the model to use. Example: "IAB_en" by default = "IPTC_en"
model = 'IAB_en'

# @param license_key - Your license key (found in the subscription section in https://www.meaningcloud.com/developer/)
license_key = 'edfe9a8fa03b720d7d25af7fb2bfbb1d'

# def extracTopic(text):

# @param text - Text to use for different API calls
# text = 'Barack Hussein Obama II  is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, he was the first African-American president of the United States. He previously served as a U.S. senator from Illinois from 2005 to 2008 and an Illinois state senator from 1997 to 2004. Obama was born in Honolulu, Hawaii. After graduating from Columbia University in 1983, he worked as a community organizer in Chicago. In 1988, he enrolled in Harvard Law School, where he was the first black person to head the Harvard Law Review. After graduating, he became a civil rights attorney and an academic, teaching constitutional law at the University of Chicago Law School from 1992 to 2004. Turning to elective politics, he represented the 13th district from 1997 until 2004 in the Illinois Senate, when he ran for the U.S. Senate. Obama received national attention in 2004 with his March Senate-primary win, his well-received July Democratic National Convention keynote address, and his landslide November election to the Senate. In 2008, he was nominated for president a year after his presidential campaign began, and after close primary campaigns against Hillary Clinton.'

def extractTopic(text):
    try:
        results = []
        # We are going to make a request to the Topics Extraction API
        topics_response = meaningcloud.TopicsResponse(meaningcloud.TopicsRequest(license_key, txt=text, lang='en',
                                                                                 topicType='e').sendReq())

        # If there are no errors in the request, we print the output
        if topics_response.isSuccessful():
            # print("\nThe request to 'Topics Extraction' finished successfully!\n")

            entities = topics_response.getEntities()
            if entities:
                # print("\tEntities detected (" + str(len(entities)) + "):\n")
                for entity in entities:
                    # print("\t\t" + topics_response.getTopicForm(entity) + ' --> ' +  topics_response.getTypeLastNode(topics_response.getOntoType(entity)) + "\n")
                    results.append([topics_response.getTopicForm(entity), topics_response.getTypeLastNode(topics_response.getOntoType(entity))])

                return results

            else:
                print("\tNo entities detected!\n")
        else:
            if topics_response.getResponse() is None:
                print("\nOh no! The request sent did not return a Json\n")
            else:
                print("\nOh no! There was the following error: " + topics_response.getStatusMsg() + "\n")

    except ValueError:
        e = sys.exc_info()[0]
        print("\nException: " + str(e))