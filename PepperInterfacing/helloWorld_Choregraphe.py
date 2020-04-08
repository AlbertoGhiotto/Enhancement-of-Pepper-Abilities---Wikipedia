import naoqi
from naoqi import ALProxy
import wikipedia
import unicodedata # To convert unicode (read from wikipedia) to string
import time
from mediawiki import MediaWiki
from recognizer import Recognizer
import sys
import functools
import argparse

def print_sections(sections, level=0):
    for s in sections:
        print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
        print_sections(s.sections, level + 1)

#IP = "130.251.13.158"
IP = "127.0.0.1"


port = 61972

# Manage audio inputs and outputs, it is used by all other audio modules
#audio_module = ALProxy("ALAudioDevice", IP, port)
mem_module = ALProxy("ALMemory", IP, port)

# Connects to speech proxy to make the robot speak
speak_module = ALProxy("ALTextToSpeech", IP, port)

# Connection to ALAnimatedSpeech proxy: it can create more lively speech by annotating the text yourself with some instructions or by adding animations for some words with ALSpeakingMovement
animated_module = ALProxy("ALAnimatedSpeech", IP, port)

# Connects to movement service to give the autonomous ability while speaking(enabled by default)
# movement_module = ALProxy("ALSpeakingMovement", IP, port)

# Connects to tablet proxy to display image
#tablet_module = ALProxy("ALTabletService", IP, port)

# Connect to dialogue proxy, we need to create and upload a .top file
dialogue_module = ALProxy("ALDialog", IP, port)
dialogue_module.setLanguage("English")  # Set the language

# Connects to speech proxy to make the robot understand what a human says
#understand_module = ALProxy("ALSpeechRecognition", IP, port)
#understand_module.setLanguage("English")  # Set the language

# Define the keyword
keyword = "Barack Obama"
vocabulary = ["yes", "no"]
vocabulary.append(keyword)

# Use MediaWiki API to extract sections since the other wikipedia API doesn't work
wikipedia = MediaWiki()
wikiPage = wikipedia.page(keyword)
sections = wikiPage.sections
print(sections)

# Load and access data from full Wikipedia pages
ny = wikipedia.page(keyword)
imageStr = unicodedata.normalize('NFKD', ny.images[2]).encode('ascii','ignore') # To get the image
content = unicodedata.normalize('NFKD', wikipedia.summary(keyword, sentences=1)).encode('ascii','ignore') # To read the first phrase

#categories = ny.categories
#print(ny.categories)
#print(wikipedia.WikipediaPage(keyword).section("Early life and career"))

time.sleep(2)

# Add the sections into the vocabulary
vocabulary.extend(sections)  # We use extend to append a list to another list
#understand_module.setVocabulary(vocabulary, False)
speak_module.say(keyword)

# Display the image on the tablet
#tablet_module.showImage(imageStr)
time.sleep(5)
#tablet_module.hideImage()

# Say the summary
speak_module.say(content)

time.sleep(1)

# Starting the recognizer
rec = Recognizer(IP)

while True:
    speak_module.say("Do you want more information?")

    # Listening for the answer
    user_input = rec.listen()
    rec.cleanMemory()
    print user_input

    if user_input == "yes":
        speak_module.say("Great! Which one of the following topic would you like to know more about?")
        for i in sections:
            speak_module.say(i)
            print i

        # Listening for the answer
        user_input_section = rec.listen()
        rec.cleanMemory()
        print user_input_section

        section_summary = unicodedata.normalize('NFKD', wikipedia.summary(ny.section(user_input_section), sentences=1)).encode('ascii','ignore')
        break


    elif user_input == "no":
        speak_module.say("Ok.")
        break

    else:
        speak_module.say("I'm sorry I didn't get that. Please answer yes or no.")
        pass


# understand_module.subscribe("WordRecognized")
# # speechRecognized = mem_module.subscriber("WordRecognized")
# stopped = False

# try:
#     while not stopped:
#         word = mem_module.getData("WordRecognized")
#         if len(word) > 0:
#             if word[0] == "yes":
#                 speak_module.say("Great! Which one of the following topic would you like to know more about?")
#                 speak_module.say(sections)
#                 stopped = True
#             elif word[0] == "no":
#                 speak_module.say("Ok.")
# except KeyboardInterrupt:
#
#     sys.exit()

# def onSpeechRecognized(msg, value):
#     print type(value)
#     print type(value[0])
#     if value[1] > 0.4:
#         got_keyword = value[0][6:-6]

# id_speechRecognized = speechRecognized.signal.connect(functools.partial(onSpeechRecognized, "WordRecognized"))