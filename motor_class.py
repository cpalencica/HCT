import RPi.GPIO as GPIO

from time import sleep
import threading
import re



class Motor:
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.MotorDir = 13

        self.MotorStep = 17
        self.MotorEn = 7
        self.StepDelay = 0.0003 #0.0003
        self.Distance = 0
        
        self.Button = 14
        GPIO.setup(self.MotorDir, GPIO.OUT)
        GPIO.setup(self.MotorStep, GPIO.OUT)
        GPIO.setup(self.MotorEn, GPIO.OUT)
        
        GPIO.setup(self.Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.MotorDir, GPIO.LOW)  
        GPIO.output(self.MotorStep, GPIO.LOW)
        GPIO.output(self.MotorEn, GPIO.LOW)
        
        
        
    
    def start(self):
        GPIO.output(self.MotorEn,GPIO.HIGH)
    
    def stop(self):
        GPIO.output(self.MotorEn,GPIO.LOW)
    
    def move(self):
        while True:
            distFromHome = self.readDist()
            choice = input('Please enter a command and a distance, e.g "f 1000":\nType "end" to stop moving: ')
            pattern = r'([A-Za-z]+)(?:\s+(\d+))?'
            match = re.match(pattern, choice)
            
            if match:
                com = mtch.group(1)
                dist = match.group(2)
                if dist:
                    dist = int(dist)
                    if com == 'f':
                        GPIO.output(self.MotorDir,GPIO.LOW)
                        direction = 'up'
                    if com == 'r':
                        if distFromHome - dist <0:
                            dist = distFromHome
                        GPIO.output(self.MotorDir,GPIO.HIGH)
                        direction = 'down'
                else:
                    if com=='h':
                        dist = self.readDist()
                        GPIO.output(self.MotorDir,GPIO.HIGH)
                        
                        direction = 'down'
                    if com =='end':
                        break
            else:
                print('Command not recognized, enter either (f)orward,(r)everse, or (h)ome')
                #continue
            for i in range(dist):
                #print('index: ',i)
                GPIO.output(self.MotorStep,GPIO.HIGH)
                sleep(self.StepDelay)
                GPIO.output(self.MotorStep,GPIO.LOW)
                sleep(self.StepDelay)
                if direction == 'up':
                    self.Distance += 1
                if direction == 'down':
                    self.Distance -= 1
                
                if self.Distance >=100000:
                    self.motorStop()
                    print("Upper limit reached.")
                    return
            with open('distance.txt','w') as file:
                file.write(str(self.Distance))
           
        
            
    def readDist(self):
        with open('distance.txt','r')as file:
            line = file.readline()
        distFromHome = line.strip('\n')
        distFromHome  = int(distFromHome)
        return distFromHome
        

    def moveUp(self,steps):
        self.start()
        GPIO.output(self.MotorDir,GPIO.LOW)
        for i in range(steps):
            self.Distance += 1
            if self.Distance >= 8495:
                print('Maximum height reached')
                self.stop()
                return False
                
            GPIO.output(self.MotorStep,GPIO.HIGH)
            sleep(self.StepDelay)
            GPIO.output(self.MotorStep,GPIO.LOW)
            sleep(self.StepDelay)
            
            #self.Distance += 1
        self.stop()
        return True
        
    def moveDown(self,steps):
        
        self.start()
        
        distFromHome = self.readDist()
        if distFromHome - steps <0:
            steps = distFromHome
        GPIO.output(self.MotorDir,GPIO.HIGH)
        for i in range(steps):
            if GPIO.input(self.Button) == GPIO.LOW:
                print('Bottom reached')
                return False
                
            GPIO.output(self.MotorStep,GPIO.HIGH)
            sleep(self.StepDelay)
            GPIO.output(self.MotorStep,GPIO.LOW)
            sleep(self.StepDelay)
            
            self.Distance -= 1
        self.stop()
        return True
    
    def home(self):
        GPIO.output(self.MotorDir,GPIO.LOW)
        self.start()
        
        for i in range(5):
            GPIO.output(self.MotorStep,GPIO.HIGH)
            sleep(self.StepDelay)
            GPIO.output(self.MotorStep,GPIO.LOW)
            sleep(self.StepDelay)
        sleep(.3)
        GPIO.output(self.MotorDir,GPIO.HIGH)
        while (GPIO.input(self.Button) != GPIO.LOW):
            GPIO.output(self.MotorStep,GPIO.HIGH)
            sleep(self.StepDelay)
            GPIO.output(self.MotorStep,GPIO.LOW)
            sleep(self.StepDelay)
            
        
        self.stop()
        
    def testButton(self):
        print('testing button....')
        while(True):
            sleep(.1)
            if GPIO.input(self.Button) == GPIO.LOW:
                print('button was pushed!')
            
            
            else:
                print('button was not pushed.')
    
    def cleanUp(self):
        GPIO.cleanup()
    
    def test(self):
        
        self.home()
        
        
        while(14000 >= self.Distance):
            self.moveUp(1000)
            

    
