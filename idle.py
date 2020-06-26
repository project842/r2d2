# R2D2 idle state script
# Randomly rotates the head and randomply plays a WAV file on an infinite loop
# Assumes the use of an L298N motor controller

# Copyright 2020 Sean Fields/Project842

# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import sys
import time
import random
import RPi.GPIO as GPIO
import pyaudio
import wave
import glob
from threading import Thread

#set GPIO pins 
in1 = 24
in2 = 23
en = 25

#location of the WAV files
sounds="/home/pi/Chatter/*.wav"

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(50)

	
def lookaround():
    while (1):
        #randomly selects which pin to activate
        direction=random.choice([in1, in2])
        #randomly selects the duty cycle percentage to apply to the motor
        speed=random.choice([50, 75, 100])
        #randomly selects the duration of the movement from 0.5 to 2 seconds
        duration=random.uniform(0.5, 2)
        #randomly selects how long to wait before executing the next move from 0 to 10 seconds
        delay=random.randrange(10)
        
        p.ChangeDutyCycle(speed)
        GPIO.output(direction, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(direction, GPIO.LOW)
        time.sleep(delay)

def talktoself():
    while (1):
        #randomly sets the delay before playing another sound.  Decrease this value to make R2 more talkative
        delay=random.randrange(30)
        #grabs the contents of the sounds directory and creates an array object from them
        soundfiles = glob.glob(sounds)
        #randomly selects a filename from the soundfiles array
        filename = random.choice(soundfiles)
        #opens and plays the filename using pyaudio
        chunk = 1024  
        wf = wave.open(filename, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                     channels = wf.getnchannels(),
                     rate = wf.getframerate(),
                     output = True)
     
        data = wf.readframes(chunk)
     
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)
     
        stream.close()
        p.terminate()
        time.sleep(delay)
     
if __name__ == "__main__":
    #set up and start the head movement on one thread
    t1 = Thread(target = lookaround)
    t1.setDaemon(True)
    t1.start()
    #set up and start the 
    t2 = Thread(target = talktoself)
    t2.setDaemon(True)
    t2.start()
    while True:
        pass

GPIO.cleanup()