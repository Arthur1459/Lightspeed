# Lightspeed Game

#### Author : Arthur Oudeyer

### How to try the game :

First of all **clone / download this repository**:
- clone : choose a folder and then clone `git clone https://github.com/Arthur1459/Lightspeed` 
- download : green button "code" -> "download zip"

Then two possibilities :

- Create the **executable** : (! only tested on Mac M1 !)
  1. make sure to have `python3` and so `pip3` installed on your computer.
  2. make sur to have installed `make` 
     - linux `sudo apt-get make`
     - mac `brew install make`
  3. in a terminal go to  `lightspeed/src`
  4. create the executable : ``make make-app``
  5. launch the app created in the `/src/dist` folder.


- Launch the **main.py** file (should works for everyone):
  1. make sure to have `python3` installed on your computer.
  2. make sur to have installed `make` 
     - linux `sudo apt-get make`
     - mac `brew install make`
  3. in a terminal go to  `lightspeed/src`
  4. install the required libraries : `make download-requirements`
  5. run `main.py` file with python : `python3 main.py`