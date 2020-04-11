#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import meaningcloud
import re

# @param model str - Name of the model to use. Example: "IAB_en" by default = "IPTC_en"
model = 'IAB_en'

# @param license_key - Your license key (found in the subscription section in https://www.meaningcloud.com/developer/)
license_key = 'edfe9a8fa03b720d7d25af7fb2bfbb1d'

# @param text - Text to use for different API calls
# text = 'Barack Hussein Obama II is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, he was the first African-American president of the United States. He previously served as a U.S. senator from Illinois from 2005 to 2008 and an Illinois state senator from 1997 to 2004. Obama was born in Honolulu, Hawaii. After graduating from Columbia University in 1983, he worked as a community organizer in Chicago. In 1988, he enrolled in Harvard Law School, where he was the first black person to head the Harvard Law Review. After graduating, he became a civil rights attorney and an academic, teaching constitutional law at the University of Chicago Law School from 1992 to 2004. Turning to elective politics, he represented the 13th district from 1997 until 2004 in the Illinois Senate, when he ran for the U.S. Senate. Obama received national attention in 2004 with his March Senate-primary win, his well-received July Democratic National Convention keynote address, and his landslide November election to the Senate. In 2008, he was nominated for president a year after his presidential campaign began, and after close primary campaigns against Hillary Clinton.'
# text = "Metroid is a science fiction action game franchise created by Nintendo. The series is primarily produced by the company's first-party developers Nintendo R&D1 and Retro Studios, although some games have been handled by other developers, including Fuse Games, Team Ninja, Next Level Games, and MercurySteam. Metroid follows space-faring bounty hunter Samus Aran, who protects the galaxy from the Space Pirates and their attempts to harness the power of the parasitic Metroid creatures. Metroid combines the platforming of Super Mario Bros."
# text = "Adolf Hitler was a German politician and leader of the Nazi Party . He rose to power as the chancellor of Germany in 1933 and then as Führer in 1934. During his dictatorship from 1933 to 1945, he initiated World War II in Europe by invading Poland on 1 September 1939. He was closely involved in military operations throughout the war and was central to the perpetration of the Holocaust."


def textSummarization(text):
    try:
        # We are going to make a request to the Topics Extraction API
        summarization_response = meaningcloud.SummarizationResponse(meaningcloud.SummarizationRequest(license_key, txt=text).sendReq())
        # summarization_response = meaningcloud.TopicsResponse(meaningcloud.TopicsRequest(license_key, txt=text, lang='en',
        #                                                                          topicType='e').sendReq())

        # If there are no errors in the request, we print the output
        if summarization_response.isSuccessful():
            #print("\nThe request to 'Text Summarization' finished successfully!\n")

            summary = summarization_response.getSummary()
            if summary:
                # print(text)
                # print(summary)
                summary = re.sub("[\(\[].*?[\)\]]", "", summary)
                return summary
            else:
                print("\tNo entities detected!\n")
        else:
            print("The summarization request didn't work")

    except ValueError:
        e = sys.exc_info()[0]
        print("\nException: " + str(e))
