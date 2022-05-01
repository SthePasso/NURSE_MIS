#from typing import final
#import matplotlib.pyplot as plt
#import tensorflow as tf
#import matplotlib.image as mpimg
import numpy as np
import base64
#import PIL
from PIL import Image
#from scipy import ndimage, misc
import codecs,json
#import math
import picamera
import picamera.array

    
class NurseMis:
    #Atributes: arms, legs, location, health, mood, head, mouth, eyes
    arm = 0
    leg = 2
    mouth = "Hey... I'm Greg..."
    health = 100
    mood = 0
    Interest = 0 # starts with no interest at all in features within his/her action space
    eyes = 2 # has two eyes that are able to sense dangers and other things
    head = 1
    strength = 50 # ranges from 1 to 100 and will change based on interactions with environment.
    gnome_name = "Greg"
    xlocation = 2 # call gamearea len(gamearea)//2 gives the central point if it is an odd number of cols or rows
    ylocation = 2
    DistanceFromHome = 0
    dictionary = {'w':0, 'a':1, 's':2, 'd':3}
    backwards = ['w','a','s','d']
    couter = 0

    #Constructor
    def __init__(self,gnome_name, mouth):
        self.gnome_name = gnome_name
        self.mouth = mouth


    # Gets and Sets
    def getImageJson(self, imgJSON):
        imgLIST = json.loads(imgJSON)
        imgNP = np.array(imgLIST)
        
        #print(imgJSON)
        #print("Next:", imgLIST)
        #print("Numpy:", type(imgNP), imgNP.shape)

        imgIMG = Image.fromarray(imgNP.astype('uint8'))
        #print(imgIMG)
        return imgIMG

    def getImage(self):
        #image = [[1,2],[3,4]]
        #print(json.dumps(image))
        with picamera.PiCamera() as camera:
            with picamera.array.PiRGBArray(camera) as output:
                camera.resolution = (64,64)
                camera.capture(output, 'rgb')
                #print('Captured %dx%d image' % (output.array.shape[1], output.array.shape[0]))
                #print(output.array)
                image = output.array
        pilimage = Image.fromarray(image).resize((24,24))
        b = image.tolist() # nested lists with sam,e data, indices
        #img = np.array([[1,2],[3,4]])
        #b = img.tolist()
        return json.dumps(np.array(pilimage).tolist())
        #return json.dumps(image)
    #arm
    def getArm(self):
        return self.arm
    def setArm(self, newArm):
        self.arm = newArm

    #leg
    def getLeg(self):
        return self.leg
    def setLeg(self,newLeg):
        self.leg = newLeg

    #head
    def getArm(self):
        return self.arm
    def setArm(self, newArm):
        self.arm = newArm

    #mouth for talking
    def getMouth(self):
        return self.mouth
    def setMouth(self, newMouth):
        self.mouth = newMouth

    #eyes
    def getEyes(self):
        return self.eyes
    def setEyes(self, newEyes):
        self.eyes = newEyes



    #secondary conditions
    #strength
    def getStrength(self):
        return self.Strength
    def setStrength(self, newStrength):
        self.strength = newStrength
    #mood
    def getMood(self):
        return self.mood
    def setMood(self, newMood):
        self.mood = newMood
    #speed of movement
    def getStrength(self):
        return self.Strength
    def setStrength(self, newStrength):
        self.strength = newStrength

    #mood
    #x,y location

    #getting x,y coordinate
    def getXlocationRobot(self):
        return self.xlocation# init

    def getYlocationRobot(self):
        return self.ylocation



    def getInterest(self):
        return self.Interest
    def setInterest(self, newInterest):
        self.interest = newInterest

    #setting x,y coordinate
    def setXlocationRobot(self,newXloc):
        self.xlocation = newXloc # init
    def setYlocationRobot(self,newYloc):
        self.ylocation = newYloc

    #distance from its home shelter in the space
    def getDistanceFromHome(self):
        return self.DistanceFromHome
    def setDistanceFromHome(self, newDistanceFromHome):
        self.DistanceFromHome = newDistanceFromHome

    #name
    def getName(self):
        return self.gnome_name
    def setName(self,newName):
        self.gnome_name = newName

    #Methods:
    '''
    talk - asking gnome to talk or say something.
    move
    decide # a binary choice about moving
    eat
    later on add drink
    sleep
        turning on
        turning off
    later on add attack
    later on add defend

    '''

    def talk(self):
        #print(self.mouth) this is an error
        print(self.getMouth())

    def moveUp(self): #w a s d
        try:
          return (self.getXlocationRobot(), self.getYlocationRobot()-1)
        except Exception:
          print("cannot perform action")
        
    def moveDown(self): #w a s d
        try:
          return (self.getXlocationRobot(), self.getYlocationRobot()+1)
        except Exception:
          print("cannot perform action")
    def moveLeft(self): #w a s d
        try:
          return (self.getXlocationRobot()-1, self.getYlocationRobot())
        except Exception:
          print("cannot perform action")
    def moveRight(self): # w a s d
        try:
          return (self.getXlocationRobot()+1, self.getYlocationRobot())
        except Exception:
          print("cannot perform action")


    def move(self,Game_Area): 
      # x origin is [2,2]
      #x = int(input("Steps in X direction: "))
      #y = int(input("Steps in Y direction: "))
        print("Where do you want to move [w,a,s,d]? ") # this is a waypoint 
        moveTo = 'w' # init
        while moveTo in ['w','a','s','d']:
            moveTo = input(":") # publish
            try:
                if(moveTo == 'w'):
                    x, y = self.moveUp()
                elif(moveTo == 'a'):
                    x,y = self.moveLeft()
                elif(moveTo == 's'):
                    x,y = self.moveDown()
                elif(moveTo == 'd'):
                    x,y = self.moveRight()
                else:
                    print("not a direction")
                    x = 'n/a'
                    y = 'n/a'
                    break
            except Exception:
                print("Exception...")
            finally:
                self.setXlocationRobot(x)
                self.setYlocationRobot(y)
                currentX = self.getXlocationRobot()
                currentY = self.getYlocationRobot()
        # Subscribe
        print(f'[{currentX},{currentY}]')
        Game_Area.setGame_Area_Position(currentX,currentY)
        print(f'moved to --> [{currentX},{currentY}]')
        Game_Area.printGame()
        return currentX,currentY

    def movePublisher(self,Game_Area): 
        moveTo = 'w' # init
        moveTo = input("Where do you want to move [w,a,s,d]? ")
        return self.dictionary[moveTo]

    def moveSubscribe(self,newMoveTo, Game_Area):
        self.couter+=1
        if (self.couter < 4):
            return;
        elif (int(newMoveTo) < 4): 
            moveTo = self.backwards[int(newMoveTo)]
            try:
                if(moveTo == 'w'):
                    x, y = self.moveUp()
                elif(moveTo == 'a'):
                    x,y = self.moveLeft()
                elif(moveTo == 's'):
                    x,y = self.moveDown()
                elif(moveTo == 'd'):
                    x,y = self.moveRight()
                else:
                    print("not a direction")
                    x = 'n/a'
                    y = 'n/a'
            except Exception:
                print("Exception...")
            finally:
                if (x<len(Game_Area.getGame_Area()[0]) and y<len(Game_Area.getGame_Area())):
                    self.setXlocationRobot(x)
                    self.setYlocationRobot(y)
        #print(f'[{currentX},{currentY}]')
        Game_Area.setGame_Area_Position(self.getXlocationRobot(),self.getYlocationRobot())
        print(f'moved to --> [{self.getXlocationRobot()},{self.getYlocationRobot()}]')
        Game_Area.printGame()
        return self.getXlocationRobot(),self.getYlocationRobot()

    #speed of movement
    def getSpeed(self):
        return self.Speed
    def setSpeed(self, newSpeed):
        self.speed = newSpeed
        
    def run(self):
        imgJson = self.getImage()
        img = self.getImageJson(imgJson)

class ObservationSpace:

    Game_Area = [[0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,1,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]]
    Game_Name = "Tik Tak Toe"


    #Constructor
    def __init__(self,Game_Name):
        self.Game_Name = Game_Name

    #Get and Set
    def getGame_Area(self):
        return self.Game_Area
    def setGame_Area(self, newGame_Area):
        self.Game_Area = newGame_Area

    # gnome location (new)
    def setGame_Area_Position(self,x, y):
        # passing a matrix to this function 
        if(x<len(self.getGame_Area()[0]) and y<len(self.getGame_Area())):
            self.Game_Area[x][y] = 1
        else:
            print("You can't access this area.")

    def getGame_Area_Position(self,x, y):
        return self.Game_Area[x][y]

    #TODO method needed: delete previous position,
    def printGame(self):
        for row in self.Game_Area:
            print(row)
    
        game_area = self.getGame_Area()  
        plt.imshow(game_area, cmap=plt.get_cmap('gray'))
        plt.show()
    
    def printArea(self):
        game_area = self.getGame_Area()  
        for row in game_area:
            print(row)


if __name__ == '__main__':
    AnaNeri = NurseMis("Ana Neri", "Hi I am NURSE MIS!") # the first nurse in Brasil (1814)
    House = ObservationSpace("House")
    Brain = Smart("tflite_models/model_conv2d.tflite")


    print(AnaNeri.getName()) #not good
    print(AnaNeri.getArm())
    AnaNeri.talk()
    AnaNeri.run()

    #Brain.run()