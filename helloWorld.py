# -*- coding: utf-8 -*-
import naoqi
from naoqi import ALProxy
import wikipedia
import unicodedata # To convert unicode (read from wikipedia) to string
import time
from mediawiki import MediaWiki
from prova import Recognizer
import sys
import functools
import argparse


def answerQuestion(question, acceptedAnswer, model):
    print(question)
    if model == 1:
        for x in range(len(acceptedAnswer)/10):
            #speak_module.say(unicodedata.normalize('NFKD', sections[x]).encode('ascii', 'ignore'))
            print(sections[x])
        print("Another section")

    while True:

        user_answer = raw_input()

        if user_answer in acceptedAnswer:
            answer = user_answer
            return answer
        elif user_answer =="Another section":
            return "Another section"
        else:
            print("Sorry! I didn't get that!")
            if model == 1:      # corresponds to sections
                print("Please answer with just the name of the section")
                #answer = answerQuestion(question, acceptedAnswer, model)
                pass
            elif model == 2:    # corresponds to yes/no
                print("Please answer with just yes or no")
                pass
            # else:
            #     # we'll see
            #     pass




#IP = "130.251.13.158"
# IP = "127.0.0.1"
# port = 61972
#
# # Manage audio inputs and outputs, it is used by all other audio modules
# #audio_module = ALProxy("ALAudioDevice", IP, port)
# mem_module = ALProxy("ALMemory", IP, port)
#
# # Connects to speech proxy to make the robot speak
# speak_module = ALProxy("ALTextToSpeech", IP, port)
#
# # Connection to ALAnimatedSpeech proxy: it can create more lively speech by annotating the text yourself with some instructions or by adding animations for some words with ALSpeakingMovement
# animated_module = ALProxy("ALAnimatedSpeech", IP, port)
#
# # Connects to movement service to give the autonomous ability while speaking(enabled by default)
# # movement_module = ALProxy("ALSpeakingMovement", IP, port)
#
# # Connects to tablet proxy to display image
# #tablet_module = ALProxy("ALTabletService", IP, port)
#
# # Connect to dialogue proxy, we need to create and upload a .top file
# dialogue_module = ALProxy("ALDialog", IP, port)
# dialogue_module.setLanguage("English")  # Set the language

# Connects to speech proxy to make the robot understand what a human says
#understand_module = ALProxy("ALSpeechRecognition", IP, port)
#understand_module.setLanguage("English")  # Set the language

# Define the keyword
keyword = "Barack Obama"
vocabulary = ["yes", "no"]
vocabulary.append(keyword)

# Use MediaWiki API to extract sections since the other wikipedia API doesn't work
wikipedia_mediawiki = MediaWiki()
wikiPage = wikipedia_mediawiki.page(keyword)
sections = wikiPage.sections
# print(sections)

# Load and access data from full Wikipedia pages
ny = wikipedia.page(keyword)
imageStr = unicodedata.normalize('NFKD', ny.images[2]).encode('ascii','ignore') # To get the image
content = unicodedata.normalize('NFKD', wikipedia.summary(keyword, sentences=1)).encode('ascii','ignore') # To read the first phrase

#categories = ny.categories
#print(ny.categories)
#print(wikipedia.WikipediaPage(keyword).section("Early life and career"))

# time.sleep(2)

# Add the sections into the vocabulary
vocabulary.extend(sections)  # We use extend to append a list to another list
#understand_module.setVocabulary(vocabulary, False)
# speak_module.say(keyword)

# Display the image on the tablet
#tablet_module.showImage(imageStr)
# time.sleep(5)
#tablet_module.hideImage()

# Say the summary
# speak_module.say(content)
print(content)
# time.sleep(1)

# Starting the recognizer
# rec = Recognizer(IP)

while True:
    user_input = answerQuestion("Do you want more information?", ["yes", "no"], 2)

    if user_input == "yes":

        while True:

            user_input_section = answerQuestion("Great! Which one of the following topic would you like to know more about?", sections, 1)

            if user_input_section in sections:
                section_text = ny.section(user_input_section)
                data = section_text.split(". ")
                section_summary = data[0] + ". " + data[1] + ". " + data[2] + ". " + data[3] + ". " + data[4] + "."

                print(section_summary)
                user_input_section_another = answerQuestion("Do you want to know about another section?", ["yes", "no"], 2)

                if user_input_section_another == "yes":
                    print("Which section do you want to know more about?")
                    pass
                elif user_input_section_another == "no":
                    break

            elif user_input_section == "Another section":
                for x in range(len(sections)):      # This command prints all the section since the user asked more info. With pepper the idea is to display them on the tablet
                    # speak_module.say(unicodedata.normalize('NFKD', sections[x]).encode('ascii', 'ignore'))
                    print(sections[x])
                pass

        break

    elif user_input == "no":
        #speak_module.say("Ok.")
        print("Ok! Però stai calmo :)")
        break



# while True:
#     speak_module.say("Do you want more information?")
#
#     # Listening for the answer
#     user_input = rec.listen()
#     rec.cleanMemory()
#     print user_input
#
#     if user_input == "yes":
#         speak_module.say("Great! Which one of the following topic would you like to know more about?")
#         for i in sections:
#             speak_module.say(i)
#             print i
#
#         # Listening for the answer
#         user_input_section = rec.listen()
#         rec.cleanMemory()
#         print user_input_section
#
#         section_summary = unicodedata.normalize('NFKD', wikipedia.summary(ny.section(user_input_section), sentences=1)).encode('ascii','ignore')
#         break
#
#     elif user_input == "no":
#         speak_module.say("Ok.")
#         break
#
#     else:
#         speak_module.say("I'm sorry I didn't get that. Please answer yes or no.")
#         pass