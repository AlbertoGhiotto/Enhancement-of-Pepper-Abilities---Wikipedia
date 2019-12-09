# SoRob
Repository for Social Robotics' project



topic_content_1 = ("topic: ~moreInfo\n"
                   "language: en\n"
                   "proposal: Do you want to know more information?\n"
                   "u1: (yes) Great!\n"
                   "u2: (no) Ok.\n")

To get list of loaded topic 
- dialogue_module.getLoadedTopics("English")

To unload 'moreInfo' is the topic name got from the above function
- dialogue_module.unloadTopic('moreInfo')   
