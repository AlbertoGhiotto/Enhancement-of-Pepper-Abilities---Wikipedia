import naoqi
from naoqi import ALProxy
import wikipedia
import unicodedata # To convert unicode (read from wikipedia) to string
import time

#_______________________________________________________________________________________________________________
# API : http://doc.aldebaran.com/2-5/naoqi/index.html

#Manage audio inputs and outputs, it is used by all other audio modules
audio_module = ALProxy("ALAudioDevice", "130.251.13.158", 9559)

# Connects to speech proxy to make the robot understand what a human says
understand_module = ALProxy("ALSpeechRecognition", "130.251.13.158", 9559)
understand_module.setLanguage("English")  # Set the language

# Connects to speech proxy to make the robot speak
speak_module = ALProxy("ALTextToSpeech", "130.251.13.158", 9559)

# Connection to ALAnimatedSpeech proxy: it can create more lively speech by annotating the text yourself with some instructions or by adding animations for some words with ALSpeakingMovement
animated_module = ALProxy("ALAnimatedSpeech", "130.251.13.158", 9559)

#Connects to "emotional" proxy to dentify the emotion expressed by the speaker’s voice
#emotion_module = ALProxy("ALVoiceEmotionAnalysis", "130.251.13.158", 9559)

# Connects to movement service to give the autonomous ability while speaking(enabled by default)
#movement_module = ALProxy("ALSpeakingMovement", "130.251.13.158", 9559)

# Connects to tablet proxy to display image
tablet_module = ALProxy("ALTabletService", "130.251.13.158", 9559)

# Connect to dialogue proxy, we need to create and upload a .top file
#http://doc.aldebaran.com/2-5/naoqi/interaction/dialog/aldialog-api.html#aldialog-api
dialogue_module = ALProxy("ALDialog", "130.251.13.158", 9559)
dialogue_module.setLanguage("English")  # Set the language

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
keyword = ("Barack Obama")
ny = wikipedia.page(keyword) #to load and access data from full Wikipedia pages

speak_module.say("The keyword is")
speak_module.say(keyword)

# Display image
#ny.images[0]
imageStr = unicodedata.normalize('NFKD', ny.images[2]).encode('ascii','ignore')
tablet_module.showImage(imageStr)
time.sleep(10)
tablet_module.hideImage()

# Convert the output of the wikipedia toolbox from unicode to string
#content = unicodedata.normalize('NFKD', ny.content).encode('ascii','ignore') #to read all the page??
content = unicodedata.normalize('NFKD', wikipedia.summary("Barack Obama", sentences=1)).encode('ascii','ignore') #to read the first phrase
speak_module.say(content)
#Try maybe it will be also animated!!!
#animated_module.say(content)
#if it works maybe is better to use this service especially during long interactions

time.sleep(2)
speak_module.say("Do you want to know something more about")
speak_module.say(keyword)
speak_module.say("?")
#these last lines could be the strating point for the .top file

#____________________________________________________________________________
#TO HAVE A DIALOGUETHE MODULE ALDialog HAS TO BE USED
#API LINK : http://doc.aldebaran.com/2-5/naoqi/interaction/dialog/aldialog.html
#WE NEED TO CREATE A .TOP FILE AND ORGANIZE THE DIALOGUE

#http://doc.aldebaran.com/2-5/naoqi/interaction/dialog/aldialog_tuto.html#aldialog-tuto
#example
#topic: ~greetings
#language: enu

#proposal: Do you want to say something more about this argument? #or keyword but i dind t know how to use a variable in this context
   #u1: (yes) I'm so happy!
   #u1: (no) I'm so sad
   #u2: (~yes) ok ^switchFocus(myweather/.)

#topicName = dialogue_module.loadTopic("/home/nao/aldialog_test_topic_file.top")
#print topicName
#ALDialog.activateTopic(topicName)
#print ALDialog.getActivatedTopics()
#ALDialog.deactivateTopic(topicName)
#print ALDialog.getActivatedTopics()
#ALDialog.unloadTopic(topicName)

#or

#topicName = dialogue_module.loadTopic("/home/nao/aldialog_test_topic_file.top")
#print topicName
#ALDialog.activateTopic(topicName)
#ALDialog.subscribe("my_subscribe_test")
#try:
#    raw_input("speak to the robot now, press Enter when finished")
#finally:
#    ALDialog.unsubscribe("my_subscribe_test")
#    ALDialog.deactivateTopic(topicName)
#    ALDialog.unloadTopic(topicName)'

#or

#topicContent = ("topic: ~mytopic()\n"
#                "language: enu\n"
#                "proposal: hello\n"
#                "u:(hi) nice to meet you\n")
#topicName = ALDialog.loadTopicContent(topicContent)
#print topicName
#print ALDialog.getLoadedTopics("English")
#ALDialog.unloadTopic(topicName)
#print ALDialog.getLoadedTopics("English")

#pay attention in this case the subscription to a topic is not taken into account as the unload of the topic(my consideration)
#______________________________________________________________
