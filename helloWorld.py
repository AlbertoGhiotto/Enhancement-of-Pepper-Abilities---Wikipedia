import naoqi
from naoqi import ALProxy
import wikipedia
import unicodedata # To convert unicode (read from wikipedia) to string

# Connects to Pepper
tts = ALProxy("ALTextToSpeech", "130.251.13.158", 9559)

# Here you should call the listener service to extract the keyword
# For now we'll assume to have the keyword ready to be used to extract the info from wikipedia

keyword = ("Barack Obama")
ny = wikipedia.page(keyword)

# Convert the output of the wikipedia toolbox from unicode to string
content = unicodedata.normalize('NFKD', ny.content).encode('ascii','ignore')

#ny.images[0]

tts.say("The keyword is")
tts.say(keyword)

content = unicodedata.normalize('NFKD', wikipedia.summary("Barack Obama", sentences=1)).encode('ascii','ignore')

tts.say(content)
#tts.say(content)
