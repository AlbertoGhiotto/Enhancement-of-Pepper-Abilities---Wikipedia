# -*- coding: utf-8 -*-
import wikipedia
import unicodedata               # To convert unicode (read from wikipedia) to string
from mediawiki import MediaWiki
from mediawiki import exceptions
import time

def answerQuestion(question, acceptedAnswer, model):        # print the question based on the model parameter
    print(question)
    if model == 1:                                          # prints the accepted answer when asking which section the user wants to talk about
        for x in range(len(acceptedAnswer)/10):
            # speak_module.say(unicodedata.normalize('NFKD', sections[x]).encode('ascii', 'ignore'))
            print(sections[x])
        print("Another section")
    elif model == 1.5:                                      # prints the accepted answer when asking which section the user wants to talk about
        for x in range(len(acceptedAnswer)):                # in this case we print every section
            # speak_module.say(unicodedata.normalize('NFKD', sections[x]).encode('ascii', 'ignore'))
            print(sections[x])

    while True:
        user_answer = raw_input()

        if user_answer in acceptedAnswer or (user_answer == "Another section" and model != 2):               # if the user's answer is contained in the list of accepted answer
            return user_answer                                                                               # simply return it to the main program
        else:
            print("Sorry! I didn't get that!")
            if model == 1:      # corresponds to sections
                print("Please answer with just the name of the section")
                pass
            elif model == 2:    # corresponds to yes/no
                print("Please answer with just yes or no")
                pass


while True:
    # Manage the keyword
    while True:
        keyword_sentence = raw_input()

        if "is " in keyword_sentence:
            keyword_sentences = keyword_sentence.split("is ")
        elif "about " in keyword_sentence:
            keyword_sentences = keyword_sentence.split("about ")
        else:
            print("I'm sorry I didn't get that! What to you want to know?")
            continue

        keyword_sentences = keyword_sentences[1].split("?")

        keyword = keyword_sentences[0]

        # Use MediaWiki API
        wikipedia_mediawiki = MediaWiki()
        try:
            wikiPage = wikipedia_mediawiki.page(keyword)
            break
        except:
            print("The information you want are not available on wikipedia! Try with something else")
            pass

    wikiPage = wikipedia_mediawiki.page(keyword)
    sections = wikiPage.sections
    content = wikiPage.summarize(sentences=1)

    # Say the summary
    print("Great! That's what I know about " + keyword + "!")
    print(content)

    while True:
        user_input = answerQuestion("Do you want more information?", ["yes", "no"], 2)          # ask the question given in parameters

        if user_input == "yes":

            user_input_section = answerQuestion("Great! Which one of the following topic would you like to know more about?", sections, 1)
            while True:
                if user_input_section in sections:
                    section_text = wikiPage.section(user_input_section)       # get the section's text
                    data = section_text.split(". ")                     # split the text every ". " character
                    section_summary = data[0] + ". " + data[1] + ". " + data[2] + ". " + data[3] + ". " + data[4] + "."     # get the first five sentences

                    print(section_summary)                              # print the first five sentences
                    user_input_section_another = answerQuestion("Do you want to know about another section?", ["yes", "no"], 2)

                    if user_input_section_another == "yes":
                        user_input_section = answerQuestion("Which section do you want to know more about?", sections, 1)
                        pass                                            # restart the while
                    elif user_input_section_another == "no":
                        break                                           # get out of the while

                elif user_input_section == "Another section":           # this prints all the section but by restarting the while it asks again the question
                    user_input_section = answerQuestion("Here are all the sections. Which one are you interested in?", sections, 1.5)
                    pass                                                # restart the while
            break

        elif user_input == "no":
            print("Ok! Però stai calmo :)")
            break


    # We'll be here only if the user does not want to know more about the topic -> ask if the user wants some other topic
    user_another_topic = answerQuestion("Do you want to know about something else?", ["yes", "no"], 2)
    if user_another_topic == "yes":
        print("What do you want to know?")
        pass
    elif user_another_topic == "no":
        print("Ok! That's it for today, see you next time! Bye!")
        break                                                       # get out of the while