
from flask import Flask, request, render_template, Response
from rpi_camera import RPiCamera


app = Flask(__name__)

#default mode is detect faces
stream_mode  = "detect-faces"

def get_feed(camera):
    global stream_mode
    
    while True:
         
        
        if stream_mode == "detect-faces":
            frame = camera.get_frame_with_face_detect().tobytes() 

        elif stream_mode == "detect-objects":
            frame = camera.get_frame_with_object_detect().tobytes()

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

@app.route('/stream')
def stream():

    feed = Response(get_feed(RPiCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
     
    return feed


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False )
