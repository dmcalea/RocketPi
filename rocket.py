import gps

import time

import subprocess

from picamera import PiCamera
from picamera import Color

#Setup GPS
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

#Setup Timer
currentTime = time.time()
timeout = time.time() + 60 * 20

#Setup Camera
camera = PiCamera()

#Start recording w/ file named current time
camera.start_recording('/home/pi/Desktop/'+ str(currentTime) +'.h264')

#Set annotate settings
camera.annotate_text = "Starting..."
camera.annotate_foreground = Color('black')
camera.annotate_background = Color('white')
camera.annotate_text_size = 18

#Recording will continue until the timeout is reached
while time.time() < timeout:
    try:
        report = session.next()
        
        #Build overlay for camera
        if report['class'] == 'TPV':
            if all(hasattr(report, attr) for attr in ["lat", "lon", "alt", "time", "speed", "climb"]):
                

                lat = str(report.lat)
                lon = str(report.lon)

                location = "lat: " + lat + " & lon:" + lon
                rtime = "time: " + report.time
                altitude = "altitude: " + str(report.alt)
                speed = "speed: " + str(report.speed)
                climb = "climb: " + str(report.climb)
                
                details = rtime + " | " + location  + "\n" + altitude + " | " + speed + " | " + climb

                #Displays overlay over camera
                camera.annotate_text = details

                print("Recording...")
    
    except KeyError:
        pass

    #Any key press will stop recording
    except KeyboardInterrupt:
        camera.stop_recording()
        
        subprocess.call("sudo MP4Box -add /home/pi/Desktop/"+str(currentTime)+".h264 /home/pi/Desktop/"+str(currentTime)+".mp4", shell=True)
        print("Exited, Finished!")
        
        quit()

    except StopIteration:
        session = None
        print "GPSD has terminated"

camera.stop_recording()

subprocess.call("sudo MP4Box -add /home/pi/Desktop/"+str(currentTime)+".h264 /home/pi/Desktop/"+str(currentTime)+".mp4", shell=True)

print("Finished!")
