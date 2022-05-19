# Flask-coral
A Flask Coral project using servos, Raspicam, and the Coral aiy-maker-kit 

The Flask project extends the examples in the `aiy-maker-kit`, by wrapping them in a Flask app which livestreams a feed of jpges processed with Coral vision models. 
It provides a client-side interface to switch between detection modes, or none at all.
The `index.html` contains a input range slider to move a Servo attached via GPIO, that can be used to pan a Raspberry Pi camera.  It can also capture
frames. 


## Setup

This project requires the AIY Maker Kit from Coral, including the model files and vision libraries. For best results, flash a new SD card with the package pre-installed to avoid any dependency issues.

1. Follow the steps in the [Coral AIY Maker Kit](https://g.co/aiy/maker) site to get the latest SD card image.
2. Flash your SD card using the Raspberry Pi Imager, as shown in their tutorial.
3. Load the card into your Pi and boot it up.
4. Run the examples in `aiy-maker-kit` examples folder to test. 
5. Install other dependencies not included in the **aiy-maker-kit** image
    - Install Visual Studio Code (optional, but easier to work on Flask projects) 
      
      ```
       $ sudo apt-get install code
      ```
    - Install Flask (may already be included)
    
      ```
       $ sudo apt-get install python3-flask
      ```
    - Install imutils (used for livestreaming)
    
      ```
      $ sudo pip install imutils
      
      ```
    - Install [pigpio](https://abyz.me.uk/rpi/pigpio/download.html) to control a servo (skip this if you don't care about panning the camera with a servo)
    
      ```
      $ sudo apt-get install pigpio python-pigpio python3-pigpio
      ```
    
6. Clone this repo into the `aiy-maker-kit` directory:

   ```
   $ git clone ...
   ```
   
7. Connect your Raspberry Pi Camera (and servo, if you have one, to GPIO 17)

## Testing

If you have everyting installed, try running the `app.py` file directly in the VS Code editor (You will need to add an Python extension to VS Code.  VS code may prompt you to do this anyway).
Like the  `aiy-maker-kit` examples, the Flask app can be run from the Terminal. In the `Flask-coral` directory, run this command:
 ```
 $ python3 app.py
 ```
 Make sure you are connected to the internet.
 
 Open a browser window and enter the address given to you by the Terminal, usually `0.0.0.0:5001`. You can change the port to another one. 
 
 ### Things to consider
 
 - You open the app in other browsers, connected on the same network. 
 - If you are already running the app in one browser, the feed will not work on a second one.
 - You can change the directory where the images save. 
 
 ### Extensions
 
 - Add more Coral models and functions to the `raspi-video.py` 
 
