import naoqi
from naoqi import ALProxy
import wikipedia
import unicodedata # To convert unicode (read from wikipedia) to string
import time

#_______________________________________________________________________________________________________________
# API : http://doc.aldebaran.com/2-5/naoqi/index.html

#Manage audio inputs and outputs, it is used by all other audio modules

audio_module = ALProxy("ALAudioDevice", "130.251.13.158", 9559)

# Connects to speech proxy to make the robot speak
speak_module = ALProxy("ALTextToSpeech", "130.251.13.158", 9559)

# Connection to ALAnimatedSpeech proxy: it can create more lively speech by annotating the text yourself with some instructions or by adding animations for some words with ALSpeakingMovement
animated_module = ALProxy("ALAnimatedSpeech", "130.251.13.158", 9559)

# Connects to movement service to give the autonomous ability while speaking(enabled by default)
#movement_module = ALProxy("ALSpeakingMovement", "130.251.13.158", 9559)

# Connects to tablet proxy to display image
tablet_module = ALProxy("ALTabletService", "130.251.13.158", 9559)

# Connect to dialogue proxy, we need to create and upload a .top file
#http://doc.aldebaran.com/2-5/naoqi/interaction/dialog/aldialog-api.html#aldialog-api
dialogue_module = ALProxy("ALDialog", "130.251.13.158", 9559)
dialogue_module.setLanguage("English")  # Set the language

# Connects to speech proxy to make the robot understand what a human says
understand_module = ALProxy("ALSpeechRecognition", "130.251.13.158", 9559)
understand_module.setLanguage("English")  # Set the language
#____________________________________________________________________________________________________
# Here you should call the listener service to extract the keyword
# For now we'll assume to have the keyword ready to be used to extract the info from wikipedia

# Start the speech recognition engine with user Test_ASR
#understand_module.subscribe("Test_ASR")
#speak_module.say("Speech recognition engine started")
#time.sleep(10)
#understand_module.unsubscribe("Test_ASR")

#Understand how to extract a keyword
#http://doc.aldebaran.com/2-5/naoqi/audio/alspeechrecognition-tuto.html

#if(speak_module.SpeechDetected == 0)
#   keyword = ("understand_module.WordRecognized[0] wikipedia")
#____________________________________________________________________
keyword = ("Pepper(robot)")
ny = wikipedia.page(keyword) #to load and access data from full Wikipedia pages

speak_module.say("The keyword is")
speak_module.say(keyword)

# Display the image on the tablet
imageStr = unicodedata.normalize('NFKD', ny.images[2]).encode('ascii','ignore')
tablet_module.showImage(imageStr)
time.sleep(2)
tablet_module.hideImage()

# Convert the output of the wikipedia toolbox from unicode to string
#content = unicodedata.normalize('NFKD', ny.content).encode('ascii','ignore') #to read all the page??
content = unicodedata.normalize('NFKD', wikipedia.summary(keyword, sentences=1)).encode('ascii','ignore') #to read the first phrase
#speak_module.say(content)
#Try maybe it will be also animated!!!
#animated_module.say(content)
#if it works maybe is better to use this service especially during long interactions

time.sleep(1)

# Writing topics' qichat code as text strings (end-of-line characters are important!)
dialogue_module.setLanguage("English")
topicContent = ('topic: ~mytopic()\n'
                'language: enu\n'
                'u: (hello) Hello human!'
                'proposal: Do you want to know more information?\n'
                'u1: (yes) Great!\n'
                'u2: (no) Ok.\n')
topicName = dialogue_module.loadTopicContent(topicContent)
print topicName
print dialogue_module.getLoadedTopics("English")

# Activating the loaded topics
dialogue_module.activateTopic(topicName)

# Starting the dialog engine - we need to type an arbitrary string as the identifier
# We subscribe only ONCE, regardless of the number of topics we have activated
dialogue_module.subscribe('my_dialog_example')


try:
        raw_input("\nSpeak to the robot using rules from the just loaded .top file. Press Enter when finished:")
finally:
        # Stopping the dialog engine
        dialogue_module.unsubscribe('my_dialog_example')

        # Deactivating the topic
        dialogue_module.deactivateTopic(topicName)

        # Now that the dialog engine is stopped and there are no more activated topics,
        # we can unload our topic and free the associated memory
        dialogue_module.unloadTopic(topicName)


