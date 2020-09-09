import RPi.GPIO as GPIO
import time
#servo motor
import sys
import Adafruit_DHT
#webSocket
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json
#humidity
import math
#convert
from ast import literal_eval

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import cv2
is_work, is_open ,is_catch = 0,0,0

class SimpleEcho(WebSocket):        

    def handleConnected(self):
        print(self.address, 'open')
        global is_work
        global is_open
        global is_catch
        

    def handleMessage(self):
        global is_work
        global is_open
        global is_catch
        
        print('is_work',is_work)
        print('is_open',is_open)
        print('is_catch',is_catch)
        
        led_R=20
        led_Y=21
        PIR_sensor=17
        servomotor_pin =18
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_R, GPIO.OUT)
        GPIO.setup(led_Y, GPIO.OUT)
        GPIO.setup(PIR_sensor, GPIO.IN)
        GPIO.setup(servomotor_pin, GPIO.OUT)
        print("PIR Ready..")
        time.sleep(2)
        #PMW: change pulse
        p= GPIO.PWM(servomotor_pin, 50)
        sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
        
        print(len(sys.argv))
        if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
            sensor = sensor_args[sys.argv[1]]
            pin = sys.argv[2]
        else:
            #ERROR occurs HERE!!!
            print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
            print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
            sys.exit(1)
        
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        p.start(0)
        #p.ChangeDutyCycle(2.5) #0
        print("servo, humidity Ready..")
        time.sleep(2)
        
        requestObject = json.dumps(self.data)
        # requestString = '{'work':'ticket' || '1'}'
        # responseString = '{"work":"0(cam) || 2(dehumid)", "user":"name"}'

        requestString = literal_eval(requestObject)
        obj = json.loads(requestString)
        print('is_work:',is_work,'     is_open',is_open)
        print(obj["work"])
        msg = obj["work"]



        #클라이언트 메세지에서 (ticket 혹은 1) is_work[1] on/off 결정(스타일링 여부) 
        if msg == "1":
            if is_work == 0:
                print("[work1]: start sytling")
                is_work=1 #작동중임,,
            elif is_work == 1:
                print("[work1]: styling done")
                is_work=0
            responseString = '{"work":"1", "username":'+is_work+'}'

        else :
            try:
                while True:
                    ##PIR sensor
                    #Human detected && not working
                    if GPIO.input(PIR_sensor) == 1 and is_work==0:
                        GPIO.output(led_Y, 1)
                        GPIO.output(led_R, 0)
                        # type_=1
                        print("person detected, count start..")
                        time.sleep(5)
                        print("count done, [work0] start..")

                        if GPIO.input(PIR_sensor) == 1:
                            is_work=1

                            # 카메라 켜고 사람 인식 start
                            
                            # ap = argparse.ArgumentParser()
                            # ap.add_argument("-c", "--cascade", required=True,
                            #     help = "path to where the face cascade resides")
                            # ap.add_argument("-e", "--encodings", required=True,
                            #     help="path to serialized db of facial encodings")
                            # args = vars(ap.parse_args())


                            # load the known faces and embeddings along with OpenCV's Haar
                            # cascade for face detection
                            #print("[INFO] loading encodings + face detector...")
                            data = pickle.loads(open("encodings.pickle", "rb").read())
                            detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                            # initialize the video stream and allow the camera sensor to warm up
                            #print("[INFO] starting video stream...")
                            vs = VideoStream(src=0).start()
                            # vs = VideoStream(usePiCamera=True).start()
                            time.sleep(3.0)
                          
                            # start the FPS counter
                            fps = FPS().start()
                            wait_person = 0
    
                            #before_name = "Unknown"
                            # loop over frames from the video file stream
                            while True:
                                # grab the frame from the threaded video stream and resize it
                                # to 500px (to speedup processing)
                                
                                frame = vs.read()
                                print('[work0]: start resizing')
                                frame = imutils.resize(frame, width=500)
                                
                                # convert the input frame from (1) BGR to grayscale (for face
                                # detection) and (2) from BGR to RGB (for face recognition)
                                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                # detect faces in the grayscale frame
                                rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                    minNeighbors=5, minSize=(30, 30))
                                # OpenCV returns bounding box coordinates in (x, y, w, h) order
                                # but we need them in (top, right, bottom, left) order, so we
                                # need to do a bit of reordering
                                boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
                                # compute the facial embeddings for each face bounding box
                                encodings = face_recognition.face_encodings(rgb, boxes)
                                names = []
                                if not encodings:
                                    if wait_person ==0:
                                        wait_person =1
                                        time.sleep(5)
                                        continue
                                    else:
                                        print('user was here, but not now')
                                        break
                                else:
                                    wait_person = 0
                                    for encoding in encodings:
                                        # attempt to match each face in the input image to our known
                                        # encodings
                                        print('encoding start')
                                        matches = face_recognition.compare_faces(data["encodings"],
                                            encoding)
                                        name = "ghost"
                                        # check to see if we have found a match
                                        if True in matches:
                                            # find the indexes of all matched faces then initialize a
                                            # dictionary to count the total number of times each face
                                            # was matched
                                            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                                            counts = {}
                                            # loop over the matched indexes and maintain a count for
                                            # each recognized face face
                                            for i in matchedIdxs:
                                                name = data["names"][i]
                                                counts[name] = counts.get(name, 0) + 1
                                            # determine the recognized face with the largest number
                                            # of votes (note: in the event of an unlikely tie Python
                                            # will select first entry in the dictionary)
                                            name = max(counts, key=counts.get)

                                        # update the list of names
                                        names.append(name)
                                    print(names[0])

                                    # loop over the recognized faces
                                    for ((top, right, bottom, left), name) in zip(boxes, names):
                                        # draw the predicted face name on the image
                                        cv2.rectangle(frame, (left, top), (right, bottom),
                                            (0, 255, 0), 2)
                                        y = top - 15 if top - 15 > 15 else top + 15
                                        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                                            0.75, (0, 255, 0), 2)
                                    # display the image to our screen
                                    cv2.imshow("Frame", frame)
                                    key = cv2.waitKey(1) & 0xFF

                                    # do a bit of cleanup
                                    if names[0] != "ghost":
                                        print('[work0]: find',names[0])
                                    else:
                                        print('[work0]: couldnt find')
                                    cv2.destroyAllWindows()
                                    vs.stop()
                                    
                                    break
                                    # update the FPS counter
                                    #fps.update()
                                    # stop the timer and display FPS information
                                    #fps.stop()
                                    


                            # send user name
                            if wait_person ==0:
                                responseString = '{"work":"0", "username":"'+names[0]+'"}'
                                break
                            else:
                                responseString = '{"work":"1", "username":"ghost"}'
                                break
                        #else:
                            #적외선 인식작업 재개
                            #continue
                            
                    #Human not detected || working (door is opening , styling ...)
                    else:
                        GPIO.output(led_R, 1)
                        GPIO.output(led_Y, 0)
                        print("person: not detected !")
                        #survo motor
                        if is_work == 0 or is_open == 1:
                            print('[work2]: door is opened or machine not working')
                            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
                            if humidity is not None and temperature is not None:
                                print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
                                humidity = math.floor(humidity)
                                print(humidity)
                                if humidity>70:
                                    #door is closed but humidity is high-> we should open
                                    if is_open==0:
                                        print('open door')
                                        #open
                                        p.ChangeDutyCycle(7.5) #90
                                        is_open=1
                                        time.sleep(1)
                                        is_work = 1
                                        responseString = '{"work":"2", "username":"open"}'
                                        break
                                #we should close
                                else:
                                    if is_open==1:
                                        print('close door')
                                        p.ChangeDutyCycle(5.0)
                                        is_open = 0
                                        is_work = 0
                                        responseString = '{"work":"2", "username":"close"}'
                                        break
                        else:
                            print("[work2]: it is  working and it is closed")

            except KeyboardInterrupt:
                print("Stopped by User")
                p.stop()
                GPIO.cleanup()
                # type_=-1
                # responseString = '{"state":"disconnected", "type":"-1", "message":""}'
                # responseString = '{"state":"connected", "type":'+str(type_)+ '"message":'+str(successcnt)+'}'
                self.sendMessage(responseString)
        

        #메시지 내용: 인식한 사람 이름
        print("########send message########")
        # successcnt_dt=0
        print(responseString)
        self.sendMessage(responseString)
   
    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('',9999, SimpleEcho)
server.serveforever()

