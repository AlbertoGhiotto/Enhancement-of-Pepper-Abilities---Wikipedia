#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata               # To convert unicode (read from wikipedia) to string
from mediawiki import MediaWiki
import topicExtractor
import textSummarizationMC

def is_not_blank(s):
    return bool(s and s.strip())

def parenthesesRemover(sentence):
    # Returns a copy of 'sentence' with any parenthesized text removed. Nested parentheses are handled.
    result = ''
    paren_level = 0
    for ch in sentence:
        if ch == '(':
            paren_level += 1
        elif (ch == ')') and paren_level:
            paren_level -= 1
        elif not paren_level:
            result += ch

    # unicodedata.normalize('NFKD', '—').encode('ascii', 'ignore')
    # result = result.replace('\n', ' ')

    return result


def checkAnswer(answer, acceptedAnswer):            # check is one of the accepted answer is contained in the user's answer
    for i in range(len(acceptedAnswer)):
        if acceptedAnswer[i] in answer:
            return [True, acceptedAnswer[i]]        # the answer was found, return it
    return [False, False]


def answerQuestion(question, acceptedAnswer, model):        # print the question based on the model parameter
    print(question)
    if model == 1:                                          # prints the accepted answer when asking which section the user wants to talk about
        for x in range(len(acceptedAnswer)/7):
            # acceptedAnswer[x] = acceptedAnswer[x].lower()
            print(acceptedAnswer[x])
        print("another section")
        acceptedAnswer.append("another section")            # add this element to the accepted answer list in order to being able to detect it with the "checkAnswer" function
    elif model == 1.5:                                      # prints the accepted answer when asking which section the user wants to talk about
        for x in range(len(acceptedAnswer)):                # in this case we print every section
            print(acceptedAnswer[x])
    elif model == 3:                                        #
        for x in range(len(acceptedAnswer)-1):
            print(acceptedAnswer[x+1])
    while True:
        user_answer = raw_input()
        if user_answer in acceptedAnswer:                           # if the user's answer is contained in the list of accepted answer
            return user_answer                                      # simply return it to the main program
        elif checkAnswer(user_answer, acceptedAnswer)[0]:
            return checkAnswer(user_answer, acceptedAnswer)[1]
        else:
            print("Sorry! I didn't get that!")
            if model == 1 or model == 1.5:      # corresponds to sections
                print("Please answer with just the name of the section")
            elif model == 2:                    # corresponds to yes/no
                print("Please answer with just yes or no")
            elif model == 3:                     # corresponds to suggestions
                print("Please answer with just the name of the suggestion")


def keywordExtraction():
    while True:
        keyword_sentence = raw_input()

        if "is " in keyword_sentence:
            keyword_sentences = keyword_sentence.split("is ")
        elif "are " in keyword_sentence:
            keyword_sentences = keyword_sentence.split("are ")
        elif "about " in keyword_sentence:
            keyword_sentences = keyword_sentence.split("about ")
        else:
            try:
                wikipedia_mediawiki = MediaWiki()
                wikiPage = wikipedia_mediawiki.page(keyword_sentence, auto_suggest=False)
                return keyword_sentence
            except:
                try:
                    wikiPage = wikipedia_mediawiki.page(keyword_sentence)
                    return keyword_sentence
                except:
                    print("I'm sorry I didn't get that! What to you want to know?")
                    continue

        keyword_sentences = keyword_sentences[1].split("?")

        return keyword_sentences[0]


def presentSection(sections):
    user_input_section = answerQuestion("Great! Which one of the following topic would you like to know more about?", sections, 1)
    while True:
        if user_input_section in sections and user_input_section != "another section":
            user_input_section = user_input_section.capitalize()    # set the first letter uppercase for correspondence with API's format
            section_text = wikiPage.section(user_input_section)  # get the section's text
            # data = section_text.split(". ")  # split the text every ". " character
            # section_summary = data[0] + ". " + data[1] + ". " + data[2] + ". " + data[3] + ". " + data[4] + "."  # get the first five sentences
            print(section_text)
            section_text = parenthesesRemover(section_text)
            if isinstance(section_text, str):
                section_text = section_text.decode('unicode-escape')

            section_summary = textSummarizationMC.textSummarization((unicodedata.normalize('NFKD', section_text).encode('ascii', 'ignore')))
            print(section_summary)  # print the first five sentences
            print(section_text)
            user_input_section_another = answerQuestion("Do you want to know about another section?", ["yes", "no"], 2)

            if user_input_section_another == "yes":
                user_input_section = answerQuestion("Which section do you want to know more about?", sections, 1)
                pass  # restart the while
            elif user_input_section_another == "no":
                break  # get out of the while

        elif user_input_section == "another section":  # this prints all the section but by restarting the while it asks again the question
            sections.remove("another section")  # remove the element which was added for the use in "checkAnswer" function
            user_input_section = answerQuestion("Here are all the sections. Which one are you interested in?", sections, 1.5)
            pass  # restart the while


def presentSuggestion(suggestions):
    user_input_suggestion = answerQuestion("Great! Which one of the following related topic would you like to know more about?", suggestions, 3)
    while True:
        if user_input_suggestion in suggestions:
            suggestedPage = wikipedia_mediawiki.page(user_input_suggestion)
            content = suggestedPage.summarize(sentences=3)
            content = parenthesesRemover(content)
            print(content)  # print the first sentence
            break
        else:
            user_input_suggestion = answerQuestion("I'm sorry I didn't get that, please answer with just the name of the related topic", suggestions, 3)


def topicproposer(topic, type):
    if (type == "City" or type == "Country" or type == "Adm1" or type == "Continent" or type == "GeoPoliticalEntity" or type == "Park" or type =="Location" or type == "NaturalReserve"):
        print("Have you ever been in " + topic + "?")
    elif (type == "FullName" or type == "FirstName"):
        print("Have you ever heard about " + topic + "?")
    elif (type == "University"):
        print("Did you go to university?")
    elif (type == "Game"):
        print("Have you ever played " + topic + "?")
    elif (type == "SoftwareCompany" or type == "MediaCompany" or type == "RetailingCompany" or type == "TechnologyEquipmentCompany" or type == "ConsumerDurablesCompany" or type == "AutomobileCompany" or type == "IndustrianCompany" or type == "Company"):
        print("I know " + topic + "! Would you like to work for this company?")
    elif (type == "War"):
        print("Have you ever lived under a period of war?")
    elif (type == "SportsTeam"):
        print("Do you like " + topic + "?")
    elif (type == "Broadcast" or type == "Movie"):
        print("Have you ever saw " + topic + "?")
    elif (type == "Book"):
        print("Do you like reading books?")


behaviour = 0

knownTopics = ["City", "Country", "Adm1", "Continent", "GeoPoliticalEntity", "Park", "Location", "NaturalReserve",
               "University", "Game","SoftwareCompany", "MediaCompany", "RetailingCompany", "TechnologyEquipmentCompany",
               "ConsumerDurablesCompany",
               "AutomobileCompany", "IndustrianCompany", "Company", "War", "SportsTeam", "Movie", "Broadcast", "Book"]

while True:
    # Manage the keyword
    keyword = keywordExtraction()

    # Use MediaWiki API
    wikipedia_mediawiki = MediaWiki()

    while True:
        try:
            wikiPage = wikipedia_mediawiki.page(keyword, auto_suggest=False)
            break
        except:
            try:
                wikiPage = wikipedia_mediawiki.page(keyword)
                break
            except:
                print("The information you want are not available on wikipedia! Try with something else!")
                print("What do you want to know?")
                keyword = keywordExtraction()

    sections = wikiPage.sections        # get the list of section

    for x in range(len(sections)):      # detecting the empty sections
        if not is_not_blank(wikiPage.section(sections[x])):
            sections[x] = None

    sections = filter(None, sections)   # removing the empty sections

    for x in range(len(sections)):      # set the first letter lower case to being user-friendlier :) (actually for speech to text)
        sections[x] = sections[x].lower()

    content = wikiPage.summarize(sentences=4)
    content = parenthesesRemover(content)
    suggestions = wikipedia_mediawiki.search(keyword, 5, False)
    for x in range(len(suggestions)):
        suggestions[x] = suggestions[x].lower()

    # Say the summary
    print("Great! That's what I know about " + keyword + "!")
    print(content)

    topics = topicExtractor.extractTopic(unicodedata.normalize('NFKD', content).encode('ascii', 'ignore'))
    # TODO: Manage case when the no entity is detected

    while True:
        user_input = answerQuestion("Do you want more information?", ["yes", "no"], 2)          # ask the question given in parameters
        if user_input == "yes":
            if behaviour == 0:
                presentSection(sections)

            elif behaviour == 1:
                presentSuggestion(suggestions)

            elif behaviour == 2:
                for index in range(len(topics)):
                    if(topics[index][1] in knownTopics ):
                        topicproposer(topics[index][0],topics[index][1])
                        raw_input()
                        print("Oh! That's very interesting!")
                        break
                else:
                    presentSuggestion(suggestions)

            behaviour = (behaviour + 1) % 3
            break

        elif user_input == "no":
            break


    # We'll be here only if the user does not want to know more about the topic -> ask if the user wants some other topic
    user_another_topic = answerQuestion("Do you want to know about something else?", ["yes", "no"], 2)
    if user_another_topic == "yes":
        print("What do you want to know?")
        pass
    elif user_another_topic == "no":
        print("Ok! That's it for today, see you next time! Bye!")
        break                                                       # get out of the while