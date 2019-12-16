import naoqi
from naoqi import ALProxy
import wikipedia
import unicodedata # To convert unicode (read from wikipedia) to string
import time
from prova import Recognizer
import sys
import functools
import argparse


IP = "130.251.13.158"

# Manage audio inputs and outputs, it is used by all other audio modules
audio_module = ALProxy("ALAudioDevice", IP, 9559)
mem_module = ALProxy("ALMemory", IP, 9559)

# Connects to speech proxy to make the robot speak
speak_module = ALProxy("ALTextToSpeech", IP, 9559)

# Connection to ALAnimatedSpeech proxy: it can create more lively speech by annotating the text yourself with some instructions or by adding animations for some words with ALSpeakingMovement
animated_module = ALProxy("ALAnimatedSpeech", IP, 9559)

# Connects to movement service to give the autonomous ability while speaking(enabled by default)
# movement_module = ALProxy("ALSpeakingMovement", IP, 9559)

# Connects to tablet proxy to display image
tablet_module = ALProxy("ALTabletService", IP, 9559)

# Connect to dialogue proxy, we need to create and upload a .top file
dialogue_module = ALProxy("ALDialog", IP, 9559)
dialogue_module.setLanguage("English")  # Set the language

# Connects to speech proxy to make the robot understand what a human says
understand_module = ALProxy("ALSpeechRecognition", IP, 9559)
understand_module.setLanguage("English")  # Set the language

# Define the keyword
keyword = "Meatball"
vocabulary = ["yes", "no"]
vocabulary.append(keyword)

# Load and access data from full Wikipedia pages
ny = wikipedia.page(keyword)
imageStr = unicodedata.normalize('NFKD', ny.images[1]).encode('ascii','ignore') # To get the image
content = unicodedata.normalize('NFKD', wikipedia.summary(keyword, sentences=1)).encode('ascii','ignore') # To read the first phrase
sections = wikipedia.sections(keyword)  # To get the name of the sections

# Add the sections into the vocabulary
vocabulary.append(sections)
understand_module.setVocabulary(vocabulary, False)
speak_module.say(keyword)

# Display the image on the tablet
tablet_module.showImage(imageStr)
time.sleep(1)
tablet_module.hideImage()

# Say the summary
# speak_module.say(content)

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
        speak_module.say(sections)

        # Listening for the answer
        user_input_section = rec.listen()
        rec.cleanMemory()
        print user_input_section

        section_summary = unicodedata.normalize('NFKD', wikipedia.summary(wikipedia.page(keyword).section(user_input_section), sentences=1)).encode('ascii','ignore')
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