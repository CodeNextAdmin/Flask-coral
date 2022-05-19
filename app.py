
from flask import Flask, request, render_template, Response
from rpi_camera import RPiCamera
import pigpio
from datetime import datetime
import cv2
import os

SERVO_PIN = 17
"""
The pigpio library offers smoother servo performance:
$ sudo apt-get install pigpio python-pigpio python3-pigpio

NOTE:Before running, make sure to start with $ sudo pigpiod,
 or read this doc: https://gpiozero.readthedocs.io/en/stable/remote_gpio.html
     
"""
pi = pigpio.pi() 
current_frame = 0

app = Flask(__name__)

#default mode is detect faces
stream_mode  = "detect-faces"

def get_feed(camera):
    global stream_mode
    
    current_frame = camera.get_frame() #save it as a jpeg to keep it around for storing it, if in capture mode.
    
    while True:
         #detect which mode was set in the client side       
        if stream_mode == "detect-faces":
            frame = camera.get_frame_with_face_detect().tobytes() 

        elif stream_mode == "detect-objects":
            frame = camera.get_frame_with_object_detect().tobytes()
            
           # Add more options here if you want to add more detection options (and also in raspi-camera.py)

        else:
            frame = camera.get_frame().tobytes()
           
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    print("welcome")

    return render_template("index.html")

@app.route('/set_mode',  methods=['POST','GET'])
def set_mode():
    global stream_mode
    data = request.data
    data = data.decode("utf-8") #data comes in bytes; need to decode.
    
    stream_mode = data
    print(stream_mode)
    return data

@app.route('/slider', methods=['POST','GET'])
def slider():
    print("slider moved!")
    data = request.data
    data = data.decode("utf-8") #data comes in bytes; need to decode.

    #set the pulse width to the incoming slider value
    pi.set_servo_pulsewidth(SERVO_PIN, int(data)) 
    
    return data

@app.route('/capture', methods=['POST', 'GET'])
def capture():
    
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H:%M:%S")
    file_name = date_time + ".jpg"

    #image was encoded with cv2.encode, so we need to decode it. 
    jpeg = cv2.imdecode(current_frame, cv2.IMREAD_COLOR)

    #We will store pics in /captured_pics, found in the root folder.
    full_path = os.path.join(app.root_path, 'captured_pics', file_name)
    
    #Save the image
    cv2.imwrite(full_path , jpeg)
    
    #return full_path does nothing yet, but it could be use to display pic.
 
    return full_path

@app.route('/stream')
def stream():

    feed = Response(get_feed(RPiCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
     
    return feed


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False )
