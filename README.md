# Lightspeed Game

#### Author : Arthur Oudeyer

### How to try the game :

First of all **clone / download this repository**:
- clone : choose a folder and then clone `git clone https://github.com/Arthur1459/Lightspeed` 
- download : green button "code" -> "download zip"

Then two possibilities :

- Create the **executable** : (! only tested in Mac M1 !)
  1. make sure to have `python3` installed on your computer.
  2. install the required libraries :
     - ```pip3 install pygame```
     - ```pip3 install opencv-python```
     - ```pip3 install glob2```
     - ```pip3 install pyinstaller```
  3. make sur to have installed `make` 
     - linux `sudo apt-get make`
     - mac `brew install make`
  4. create the executable : ``make make-app``
  5. launch the app created in the `/src/dist` folder.


- Launch the **main.py** file (should works for everyone):
  1. make sure to have `python3` installed on your computer.
  3. install the required libraries :
     - ```pip3 install pygame```
     - ```pip3 install opencv-python```
     - ```pip3 install glob2```
  4. in a terminal go to  `lightspeed/src` or in files explorer.
  5. run `main.py` file with python : `python3 main.py`