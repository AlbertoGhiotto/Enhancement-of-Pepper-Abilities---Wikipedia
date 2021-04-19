# Enhancement of Pepper Abilities
This project aims to implement a chat bot able to manage the information contained in the wikipedia website and present them to the user in a human-like way.
The bot is able to adopt different behaviours, extract related topics from the discussed information and summarize the available related content.

This project was born as a mean to enhance the abilities of the Pepper humanoid robot but, due to COVID-19 related reasons which made the Pepper robot unavailable to the development team, its development had to pivot to a text-based solution.
Nevertheless, in the code there are the references to the NAOqi sdk, which would make possible the implementation of the developed code on the actual Pepper robot.

Please refer to the [project report](https://github.com/AlbertoGhiotto/Enhancement-of-Pepper-Abilities---Wikipedia/blob/master/Pepper_Wikipedia___Social_Robotics_Project_Report.pdf) for further details.

## Implementation
### Required Packages

Install the [wikimedia API](https://github.com/barrust/mediawiki) with:

``` pip install pymediawiki ``` 

Install the python [meaningCloud API](https://github.com/MeaningCloud/meaningcloud-python) with:

``` pip install MeaningCloud-python ``` 

### Running the chat bot

To launch the chat bot, run the ``` chatBot.py``` python script.

### Workflow
<p align="center">
 <img src="documentation/wf.png" width="650"/>
</p>


## Authors
* Francesca Canale: francesca.canale.95@gmail.com
* Tommaso Gruppi: tommygruppi@gmail.com
* Alberto Ghiotto: alberto.ghiotto@hotmail.it
