import qi
import sys
import time

class Recognizer():
    def __init__(self, ip):

        try:
            # Initialize qi framework.
            self.session = qi.Session()
            self.session.connect("tcp://" + ip + ":" + str(9559))
            print("\nConnected to Naoqi at ip \"" + ip + "\" on port " + str(9559) + ".\n")

        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + ip + "\" on port " + str(9559) + ".\n"
                                                                                                "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)

        self.pMemory  = self.session.service("ALMemory") #, "130.251.13.158", 9559)
        self.pASR     = self.session.service("ASR2") #, "130.251.13.158", 9559)
        self.speech_reco_event = "Audio/RecognizedWords"

        self.initGoogleRecognition()

    def initGoogleRecognition(self):
        '''
        Subscribe to the microevent self.speech_reco_event, which is raised by Softbank Robotics' AbcdkSoundReceiver.py
        inside the _processRemote() function whenever a sentence is recognized by Google services.
        '''
        ## If the action previously ended in a wrong away, clean up the memory
        self.cleanMemory()
        self.pMemory.subscriber(self.speech_reco_event)

    def cleanMemory(self):
        '''
        Clean Pepper's memory from the previously detected words/sentences.
        '''
        try:
            self.pMemory.insertData(self.speech_reco_event, [])
        except:
            pass

    def listen(self):
        '''
        Get the user input from Pepper's memory, recognized through Google Speech Recognition.
        Clean the memory right before returning, otherwise the same input will be returned every time this function is
        called even if the user did not talk anymore.
        '''
        self.pASR.startReco("English", False, True)
        _timeout = 15
        start_time_no_input = time.time()
        start_time_silence = time.time() + 3600

        user_input = ""
        input = None
        input = self.pMemory.getData(self.speech_reco_event)

        while True:
            while input == None or input == []:
                if time.time() - start_time_silence > 0.1:
                    return user_input
                if time.time() - start_time_no_input > _timeout:
                    return None

                input = self.pMemory.getData(self.speech_reco_event)

            sep = " " if not user_input == "" else ""
            user_input = user_input + sep + input[0][0].decode('utf-8')
            start_time_silence = time.time()
            start_time_no_input = time.time()
            self.cleanMemory()
            input = self.pMemory.getData(self.speech_reco_event)

        self.pASR.stopReco()

