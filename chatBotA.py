#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata               # To convert unicode (read from wikipedia) to string
from mediawiki import MediaWiki
from extractTopic import extractTopic
from textSummarization import textSummarization
from logA import log
from logA import closeLog
import copy


def is_not_blank(str):
    # Check if str is an empty string
    return bool(str and str.strip())


def parenthesesRemover(sentence):
    # Returns a copy of 'sentence' with any parenthesized text removed. Nested parentheses are handled
    result = ''
    paren_level = 0
    for ch in sentence:
        if ch == '(':
            paren_level += 1
        elif (ch == ')') and paren_level:
            paren_level -= 1
        elif not paren_level:
            result += ch
    return result


def checkAnswer(answer, acceptedAnswer):
    # Check if inside the user's answer there is one of the accepted answers
    for i in range(len(acceptedAnswer)):
        if acceptedAnswer[i] in answer:
            return [True, acceptedAnswer[i]]        # the answer was found, return it
    return [False, False]


def answerQuestion(question, acceptedAnswer, model):            # print the question based on the model parameter

    print(question)

    if model == 1:                                              # limited number of sections case
        if len(acceptedAnswer) < 6:
            for x in range(len(acceptedAnswer)):
                print(acceptedAnswer[x])
        else:
            for x in range(len(acceptedAnswer)/6):                  # prints the accepted answer when asking which section the user wants to talk about
                print(acceptedAnswer[x])
            print("another section")
            acceptedAnswer.append("another section")                # add this element to the accepted answer list in order to being able to detect it with the "checkAnswer" function
    elif model == 1.5:                                          # all sections case
        for x in range(len(acceptedAnswer)):                    # prints the accepted answer when asking which section the user wants to talk about
            print(acceptedAnswer[x])
    elif model == 3:                                            # suggestions case
        for x in range(len(acceptedAnswer)-1):                  # prints the accepted answer when asking which related topic the user wants to talk about
            print(acceptedAnswer[x+1])                          # not considering the first one because it corresponds to the original topic

    while True:
        user_answer = raw_input()
        user_answer = user_answer.lower()
        if user_answer in acceptedAnswer:                       # if the user's answer is exactly one of the accepted answers
            return user_answer                                  # simply return it to the main program
        elif model == 4:                                                # corresponds to the last question "Do you want to talk about something else?"
            [possibleKeyword, flag] = isThereAKeyword(user_answer)      # check if there is a keyword in the user's answer
            if flag:                                                    # flag = True means that a keyword is found
                return possibleKeyword
            elif checkAnswer(user_answer, acceptedAnswer)[0]:           # if keyword not found, check if there is "yes/no" in the user's answer
                return checkAnswer(user_answer, acceptedAnswer)[1]
            elif user_answer == "terminate":        # to terminate the test
                return user_answer
            else:                                                       # if keyword not found + there is no "yes/no"
                print("Sorry I didn't get that! Are you interested in something else?")
                continue
        elif checkAnswer(user_answer, acceptedAnswer)[0]:       # if not, check if one of the accepted answers is contained in the user's answer
            return checkAnswer(user_answer, acceptedAnswer)[1]
        else:
            print("Sorry! I didn't get that! I know it's sometimes difficult with me but don't feel discouraged!")
            if model == 1 or model == 1.5:      # corresponds to sections
                print("Please answer with just the name of the section")
            elif model == 2:                    # corresponds to yes/no
                print("Please answer with just yes or no")
            elif model == 3:                     # corresponds to suggestions
                print("Please answer with just the name of the related topic")


def checkWiki(keyword):                     # Check if it exists a wikipedia page corresponding to the keyword
    try:
        wikipedia_mediawiki = MediaWiki()   # check if exists a page corresponding to the keyword
        wikiPage = wikipedia_mediawiki.page(keyword, auto_suggest=False)
        return [True, False]                # True = the page exists, False = auto-suggest OFF
    except:
        try:
            wikiPage = wikipedia_mediawiki.page(keyword)    # check with auto-suggest
            return [True, True]             # True = the page exists, True = auto-suggest ON
        except:
            print("I'm sorry the information you want are not available on wikipedia! Try with something else!")
            return [False, False]           # False = the page doesn't exist


def isThereAKeyword(keyword_sentence):
    # Check if in the answer to the question "Do you want to know about something else?" there is a possible keyword
    if " is " in keyword_sentence:           # for questions like "Who is - ?"
        keyword_sentences = keyword_sentence.split("is ")
    elif " are " in keyword_sentence:        # for questions like "Who are the - ?"
        keyword_sentences = keyword_sentence.split("are ")
    elif " about " in keyword_sentence:      # for questions like "What do you know about - ?"
        keyword_sentences = keyword_sentence.split("about ")
    elif " in " in keyword_sentence:          # for sentences like "I'm interested in - "
        keyword_sentences = keyword_sentence.split("in ")
    elif " when " in keyword_sentence:          # for sentences like "I want to know when - "
        keyword_sentences = keyword_sentence.split("when ")
    elif " where " in keyword_sentence:         # for sentences like "I want to know where - "
        keyword_sentences = keyword_sentence.split("where ")
    else:
        return [False, False]
    keyword_sentences = keyword_sentences[1].split("?")

    return [keyword_sentences[0], True]


def keywordExtraction():                                    # Extract the keyword from user's input

    while True:
        keyword_sentence = raw_input()

        if " is " in keyword_sentence:                       # for questions like "Who is - ?"
            keyword_sentences = keyword_sentence.split("is ")
        elif " are " in keyword_sentence:                    # for questions like "Who are the - ?"
            keyword_sentences = keyword_sentence.split("are ")
        elif " about " in keyword_sentence:                  # for questions like "What do you know about - ?"
            keyword_sentences = keyword_sentence.split("about ")
        elif " in " in keyword_sentence:                     # for sentences like "I'm interested in - "
            keyword_sentences = keyword_sentence.split("in ")
        elif " when " in keyword_sentence:                   # for sentences like "I want to know when - "
            keyword_sentences = keyword_sentence.split("when ")
        elif " where " in keyword_sentence:                  # for sentences like "I want to know where - "
            keyword_sentences = keyword_sentence.split("where ")
        else:                                               # if it is not one of the patterned questions
            try:                                            # check if the question has a page on wikipedia (for example if the user inputs only the keyword)
                wikipedia_mediawiki = MediaWiki()
                wikiPage = wikipedia_mediawiki.page(keyword_sentence, auto_suggest=False)       # check without auto-suggest
                return [keyword_sentence, False]            # False = auto-suggest OFF
            except:
                try:
                    wikiPage = wikipedia_mediawiki.page(keyword_sentence)                       # check with auto-suggest
                    return [keyword_sentence, True]         # True = auto-suggest ON
                except:
                    print("I'm sorry the information you want are not available on wikipedia! Try with something else!")
                    log("keywordEX,null")
                    continue

        keyword_sentences = keyword_sentences[1].split("?")
        [page, auto_suggest] = checkWiki(keyword_sentences[0])
        if page:           # if it exists a wikipedia page about the keyword
            return [keyword_sentences[0], auto_suggest]


def presentSection(sections, actualSection):                           # Present the section chosen by the user.
    # The second parameter is used to address the sections without having issues with upper and lower case letters
    user_input_section = answerQuestion("Great! Which one of the following sections would you like to know more about?", sections, 1)
    while True:
        if user_input_section in sections and user_input_section != "another section":
            for x in range(len(actualSection)):
                if user_input_section == sections[x]:
                    user_input_section = actualSection[x]                   # get the corresponding case sensitive section

            section_text = wikiPage.section(user_input_section)             # get the section's text
            section_text = parenthesesRemover(section_text)                 # remove the parenthesis from the text

            if isinstance(section_text, str):                               # if the text is a string
                section_text = section_text.decode('unicode-escape')        # convert it to unicode

            section_summary = textSummarization((unicodedata.normalize('NFKD', section_text).encode('ascii', 'ignore')))
            print(section_summary)                                          # print the summary obtained form textSummarization API

            user_input_section_another = answerQuestion("Do you want to know about another section?", ["yes", "no"], 2)

            if user_input_section_another == "yes":
                user_input_section = answerQuestion("Which section do you want to know more about?", sections, 1)
                log("presentSection,another section,yes")
                pass    # restart the while
            elif user_input_section_another == "no":
                log("presentSection,another section,no")
                break   # get out of the while

        elif user_input_section == "another section":           # this prints all the section but by restarting the while it asks again the question
            sections.remove("another section")                  # remove the element which was added for the use in "checkAnswer" function
            log("presentSection,section chosen,another section")
            user_input_section = answerQuestion("Here are all the sections. Which one are you interested in?", sections, 1.5)
            pass     # restart the while


def presentSuggestion(suggestions):                     # Present the related topic (suggestion) chosen by the user

    user_input_suggestion = answerQuestion("Great! Which one of the following related topic would you like to know more about?", suggestions, 3)
    while True:
        if user_input_suggestion in suggestions:
            suggestedPage = wikipedia_mediawiki.page(user_input_suggestion)     # search on wikipedia the suggestion's page
            content = suggestedPage.summarize(sentences=3)                      # summarize its content
            content = parenthesesRemover(content)
            content = content.split("\n")[0]
            print(content)                                                      # print the summary
            break
        else:
            user_input_suggestion = answerQuestion("I'm sorry I didn't get that, please answer with just the name of the related topic", suggestions, 3)


def topicProposer(topic, type):                 # Propose a conversation topic based on the type of the extracted topics

    if (type == "City" or type == "Country" or type == "Adm1" or type == "Continent" or type == "GeoPoliticalEntity" or type == "Park" or type =="Location" or type == "NaturalReserve"):
        print("Have you ever been to " + topic + "?")
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

behaviour = 1
presenter = 0
question  = 0
questionTopic = 0

knownTopics = ["City", "Country", "Adm1", "Continent", "GeoPoliticalEntity", "Park", "Location", "NaturalReserve",
               "University", "Game", "SoftwareCompany", "MediaCompany", "RetailingCompany", "TechnologyEquipmentCompany",
               "ConsumerDurablesCompany",
               "AutomobileCompany", "IndustrialCompany", "Company", "War", "SportsTeam", "Movie", "Broadcast", "Book"]

needKeyword = True

while True:

    if needKeyword:
        # Manage the keyword
        [keyword, suggest] = keywordExtraction()
        log("keywordEX," + keyword)
        needKeyword = True

    # Use MediaWiki API
    wikipedia_mediawiki = MediaWiki()

    # Page
    wikiPage = wikipedia_mediawiki.page(keyword, auto_suggest=suggest)

    # Sections
    sections = wikiPage.sections            # get the list of sections

    for x in range(len(sections)):          # detecting the empty sections
        if not is_not_blank(wikiPage.section(sections[x])):
            sections[x] = None
        # if "\u0x8211" in sections[x]:     # trying to remove the sections with the - not recognised by system (e.g illinois state senator (1997–2004))
        #     sections[x] = None
    sections = filter(None, sections)       # removing the empty sections

    actualSection = copy.copy(sections)     # make a shallow copy of the list to have the case sensitive sections list

    for x in range(len(sections)):          # set the first letter lower case to being user-friendlier :) (actually for speech to text)
        sections[x] = sections[x].lower()

    # Suggestions
    suggestions = wikipedia_mediawiki.search(keyword, 5, False)     # get the related topic
    # Check that the suggested pages exist, if not, remove the suggestion from the list
    for x in range(len(suggestions)):
        try:
            suggestedPage = wikipedia_mediawiki.page(suggestions[x])  # search on wikipedia the suggestion's page
        except:
            suggestions[x] = None

    suggestions = filter(None, suggestions)  # removing the empty suggestions


    for x in range(len(suggestions)):
        suggestions[x] = suggestions[x].lower()                     # set the first letter lower case to being user-friendlier :) (actually for speech to text)

    # Content
    content = wikiPage.summarize(sentences=3)                   # get the summary of the wikipedia page
    content = parenthesesRemover(content)                       # remove the parenteses
    content = content.split("\n")[0]                            # take everything until a \n. Done to avoid going up to sections for short pages
    if presenter == 0:
        print("Great! That's what I know about " + keyword + "!")
    elif presenter == 1:
        print("Oh, I know something about this topic!")
    elif presenter == 2:
        print("I was just reading an article about " + keyword + " last day.")
    print(content)                                              # say the summary
    presenter = (presenter + 1) % 3                             # incrementing the presenter so that is not always the same

    # Topic of conversation
    topics = extractTopic(unicodedata.normalize('NFKD', content).encode('ascii', 'ignore'))      # extracting the topics from the page's content
    foundTopic = False          # flag for when no extracted topic is found

    while True:
        if behaviour != 2:
            if question == 0:
                user_input = answerQuestion("Do you want more information about this topic?", ["yes", "no"], 4)
            else:
                user_input = answerQuestion("Is there something else you would like to know about this topic?", ["yes", "no"], 4)
            question = (question + 1) % 2
        else:
            user_input = "yes"          # to make the third behaviour work without user input
            log("moreInfo," + str(behaviour) + ",null")

        if user_input == "yes":
            log("moreInfo," + str(behaviour) + ",yes")
            if behaviour == 0 and len(sections) > 0:
                presentSection(sections, actualSection)
                behaviour = (behaviour + 1) % 3  # incrementing the behaviour so that is not always the same
                restart = False
                break

            elif behaviour == 1 and len(suggestions) > 0:
                presentSuggestion(suggestions)
                behaviour = (behaviour + 1) % 3  # incrementing the behaviour so that is not always the same
                restart = False
                break

            elif behaviour == 2:
                if topics is not None:
                    for index in range(len(topics)):
                        if(topics[index][1] in knownTopics ):                   # check if in the extracted topic there is something known to ask
                            topicProposer(topics[index][0], topics[index][1])   # [0] name of the topic, [1] type of the topic
                            raw_input()                                         # answer of the user about the topic
                            print("Oh! That's very interesting!")
                            restart = False
                            foundTopic = True       # found a topic to propose to the user -> display the next print
                            break
                    if not foundTopic:
                        print("That's all I know about this topic! I'll look something up and I'll tell you, try again later!")
                        foundTopic = False
                else:
                    log("topicProposer,empty list")


                behaviour = (behaviour + 1) % 3         # incrementing the behaviour so that is not always the same
                restart = False
                break
            else:              # when there are no sections in the list and the behaviour is 0
                print("That's all I know about this topic!")
                break
        elif user_input == "no":
            log("moreInfo," + str(behaviour) + ",no")
            restart = False
            break
        else:
            [pageExist, suggest] = checkWiki(user_input)
            if pageExist:
                keyword = user_input
                needKeyword = False
                restart = True
                log("moreInfo," + str(behaviour) + ",keyword")
                break
            #else:
            #    needKeyword = True

    if restart == False:
        # We'll be here only if the user does not want to know more about the topic -> ask if the user wants some other topic
        if questionTopic == 0:
            user_another_topic = answerQuestion("Do you want to know about something else?", ["yes", "no"], 4)
        elif questionTopic == 1:
            user_another_topic = answerQuestion("Are you interested in something else?", ["yes", "no"], 4)
        else:
            user_another_topic = answerQuestion("Is there something else you would like to know?", ["yes", "no"], 4)
        questionTopic = (questionTopic + 1 ) % 3

        if user_another_topic == "yes":
            print("What do you want to know?")
            log("anotherTopic,yes")
            needKeyword = True
        elif user_another_topic == "no":
            # print("Ok! That's it for today, see you next time! Bye!")
            print("Come on, I too am quarantined and I'm bored! Ask me something else!")
            log("anotherTopic,no")
            needKeyword = True
            continue                                    # patch for continuous testing. We remove the ability
            # break               # get out of the while -> end of the program
        elif user_another_topic == "terminate":
            break
        else:
            [pageExist, suggest] = checkWiki(user_another_topic)
            if pageExist:
                keyword = user_another_topic
                needKeyword = False
                log("anotherTopic,keyword,true")
            else:
                needKeyword = True
                log("anotherTopic,keyword,false")
    else:
        continue

closeLog()