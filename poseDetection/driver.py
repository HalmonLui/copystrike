import tkinter as tk, threading
from tkinter import *
import tkinter.font
from tkinter import filedialog
from tkinter.font import *
import imageio
from imageio import *
from PIL import *
import cv2
from cv2 import *
import PIL
from PIL import Image, ImageTk
from PIL import *
import os, sys
import time
from time import *
import  json
from json import *
import requests
from requests import *
import moviepy
from moviepy import *
import moviepy.editor
from moviepy.editor import VideoFileClip
import matplotlib
from matplotlib import *
# import matplotlib.pyplot
# from matplotlib.pyplot import *
import math
from math import *
import numpy
from numpy import *


mainFile = None
fileName = None
directory = None
frames = None
video = None
video2 = None

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("Bowling Analysis")
        master.resizable(False, False)

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.categoryFont = Font(family="Times New Roman", size=14, underline=True)
        self.normalFont = Font(family="Times New Roman", size=12, underline=False)
        self.buttonFont = Font(family="Times New Roman", size=16, underline=False)

        self.labelInfo = Label(root, text="Please Enter Information:", font=self.categoryFont)
        self.labelInfo.pack()
        self.labelInfo.place(x=20, y=10, anchor=NW)

        self.labelName = Label(root, text="Name:", font=self.normalFont)
        self.labelName.pack()
        self.labelName.place(x=20, y=40, anchor=NW)

        self.labelGender = Label(root, text="Gender:", font=self.normalFont)
        self.labelGender.pack()
        self.labelGender.place(x=20, y=70, anchor=NW)

        self.labelAge = Label(root, text="Age:", font=self.normalFont)
        self.labelAge.pack()
        self.labelAge.place(x=20, y=100, anchor=NW)

        self.labelHeight = Label(root, text="Height:", font=self.normalFont)
        self.labelHeight.pack()
        self.labelHeight.place(x=20, y=130, anchor=NW)

        self.labelShoe = Label(root, text="Shoe Size:", font=self.normalFont)
        self.labelShoe.pack()
        self.labelShoe.place(x=20, y=160, anchor=NW)

        self.boxName = Text(root, height=1, width=14)
        self.boxName.pack()
        self.boxName.place(x=95, y=43, anchor=NW)

        genderChoices = ["Male", "Female"]
        self.genderMF = StringVar(root)
        self.genderMF.set("Male")
        self.boxGender = OptionMenu(root, self.genderMF, *genderChoices)
        self.boxGender.config(width=12)
        self.boxGender.pack()
        self.boxGender.place(x=95, y=68, anchor=NW)

        self.boxAge = Text(root, height=1, width=14)
        self.boxAge.pack()
        self.boxAge.place(x=95, y=103, anchor=NW)

        self.labelFeet = Label(root, text="FT:", font=self.normalFont)
        self.labelFeet.pack()
        self.labelFeet.place(x=95, y=130, anchor=NW)

        self.labelInches = Label(root, text="IN:", font=self.normalFont)
        self.labelInches.pack()
        self.labelInches.place(x=160, y=130, anchor=NW)

        self.boxFeet = Text(root, height=1, width=2)
        self.boxFeet.pack()
        self.boxFeet.place(x=125, y=133, anchor=NW)

        self.boxInches = Text(root, height=1, width=2)
        self.boxInches.pack()
        self.boxInches.place(x=190, y=133, anchor=NW)

        self.boxShoe = Text(root, height=1, width=14)
        self.boxShoe.pack()
        self.boxShoe.place(x=95, y=163, anchor=NW)

        self.startButton = Button(root, height=2, width=15, text='Start', font=self.buttonFont, command=playVideo)
        self.startButton.pack()
        self.startButton.place(x=20, y=200)

        self.restartButton = Button(root, height=2, width=15, text='Restart', font=self.buttonFont,
                                    command=restartVideo)
        self.restartButton.pack()
        self.restartButton.place(x=225, y=200)

        self.fileButton = Button(root, height=1, width=4, text='File:', font=self.normalFont, command=selectFile)
        self.fileButton.pack()
        self.fileButton.place(x=230, y=36, anchor=NW)

        self.fileBox = Text(root, height=1, width=14)
        self.fileBox.pack()
        self.fileBox.place(x=305, y=43, anchor=NW)

        self.labelFrames = Label(root, text="Frames:", font=self.normalFont)
        self.labelFrames.pack()
        self.labelFrames.place(x=230, y=70, anchor=NW)

        self.framesBox = Text(root, height=1, width=14)
        self.framesBox.pack()
        self.framesBox.place(x=305, y=73, anchor=NW)

        self.labelPerceived = Label(root, text="Perceived Values:", font=self.categoryFont)
        self.labelPerceived.pack()
        self.labelPerceived.place(x=500, y=10, anchor=NW)

        self.labelRknee = Label(root, text="Right Leg Angle at Release:", font=self.normalFont)
        self.labelRknee.pack()
        self.labelRknee.place(x=500, y=40, anchor=NW)

        self.answerRknee = Label(root, text="", font=self.normalFont)
        self.answerRknee.pack()
        self.answerRknee.place(x=725, y=40, anchor=NE)

        self.labelRelbow = Label(root, text="Right Arm Angle at Release:", font=self.normalFont)
        self.labelRelbow.pack()
        self.labelRelbow.place(x=500, y=70, anchor=NW)

        self.answerRelbow = Label(root, text="", font=self.normalFont)
        self.answerRelbow.pack()
        self.answerRelbow.place(x=725, y=70, anchor=NE)

        self.labelLknee = Label(root, text="Left Leg Angle at Release:", font=self.normalFont)
        self.labelLknee.pack()
        self.labelLknee.place(x=500, y=100, anchor=NW)

        self.answerLknee = Label(root, text="", font=self.normalFont)
        self.answerLknee.pack()
        self.answerLknee.place(x=725, y=100, anchor=NE)

        self.labelLelbow = Label(root, text="Left Arm Angle at Release:", font=self.normalFont)
        self.labelLelbow.pack()
        self.labelLelbow.place(x=500, y=130, anchor=NW)

        self.answerLelbow = Label(root, text="", font=self.normalFont)
        self.answerLelbow.pack()
        self.answerLelbow.place(x=725, y=130, anchor=NE)

        self.labelBack = Label(root, text="Back Angle at Release:", font=self.normalFont)
        self.labelBack.pack()
        self.labelBack.place(x=500, y=160, anchor=NW)

        self.answerBack = Label(root, text="", font=self.normalFont)
        self.answerBack.pack()
        self.answerBack.place(x=725, y=160, anchor=NE)

        self.labelVelocity = Label(root, text="Ball Velocity at Release:", font=self.normalFont)
        self.labelVelocity.pack()
        self.labelVelocity.place(x=500, y=190, anchor=NW)

        self.answerVelocity = Label(root, text="", font=self.normalFont)
        self.answerVelocity.pack()
        self.answerVelocity.place(x=725, y=190, anchor=NE)



        self.labelRkneeLS = Label(root, text="Right Leg Angle at Last Step:", font=self.normalFont)
        self.labelRkneeLS.pack()
        self.labelRkneeLS.place(x=750, y=40, anchor=NW)

        self.answerRkneeLS = Label(root, text="", font=self.normalFont)
        self.answerRkneeLS.pack()
        self.answerRkneeLS.place(x=1000, y=40, anchor=NE)

        self.labelRelbowLS = Label(root, text="Right Arm Angle at Last Step:", font=self.normalFont)
        self.labelRelbowLS.pack()
        self.labelRelbowLS.place(x=750, y=70, anchor=NW)

        self.answerRelbowLS = Label(root, text="", font=self.normalFont)
        self.answerRelbowLS.pack()
        self.answerRelbowLS.place(x=1000, y=70, anchor=NE)

        self.labelLkneeLS = Label(root, text="Left Leg Angle at Last Step:", font=self.normalFont)
        self.labelLkneeLS.pack()
        self.labelLkneeLS.place(x=750, y=100, anchor=NW)

        self.answerLkneeLS = Label(root, text="", font=self.normalFont)
        self.answerLkneeLS.pack()
        self.answerLkneeLS.place(x=1000, y=100, anchor=NE)

        self.labelLelbowLS = Label(root, text="Left Arm Angle at Last Step", font=self.normalFont)
        self.labelLelbowLS.pack()
        self.labelLelbowLS.place(x=750, y=130, anchor=NW)

        self.answerLelbowLS = Label(root, text="", font=self.normalFont)
        self.answerLelbowLS.pack()
        self.answerLelbowLS.place(x=1000, y=130, anchor=NE)

        self.labelBackLS = Label(root, text="Back Angle at Last Step:", font=self.normalFont)
        self.labelBackLS.pack()
        self.labelBackLS.place(x=750, y=160, anchor=NW)

        self.answerBackLS = Label(root, text="", font=self.normalFont)
        self.answerBackLS.pack()
        self.answerBackLS.place(x=1000, y=160, anchor=NE)

        self.labelVelocityLS = Label(root, text="Ball Velocity at Last Step:", font=self.normalFont)
        self.labelVelocityLS.pack()
        self.labelVelocityLS.place(x=750, y=190, anchor=NW)

        self.answerVelocityLS = Label(root, text="", font=self.normalFont)
        self.answerVelocityLS.pack()
        self.answerVelocityLS.place(x=1000, y=190, anchor=NE)



        self.labelRkneeSS = Label(root, text="Right Leg Angle at 2nd to Last Step:", font=self.normalFont)
        self.labelRkneeSS.pack()
        self.labelRkneeSS.place(x=1000, y=40, anchor=NW)

        self.answerRkneeSS = Label(root, text="", font=self.normalFont)
        self.answerRkneeSS.pack()
        self.answerRkneeSS.place(x=1275, y=40, anchor=NE)

        self.labelRelbowSS = Label(root, text="Right Arm Angle at 2nd to Last Step:", font=self.normalFont)
        self.labelRelbowSS.pack()
        self.labelRelbowSS.place(x=1000, y=70, anchor=NW)

        self.answerRelbowSS = Label(root, text="", font=self.normalFont)
        self.answerRelbowSS.pack()
        self.answerRelbowSS.place(x=1275, y=70, anchor=NE)

        self.labelLkneeSS = Label(root, text="Left Leg Angle at 2nd to Last Step:", font=self.normalFont)
        self.labelLkneeSS.pack()
        self.labelLkneeSS.place(x=1000, y=100, anchor=NW)

        self.answerLkneeSS = Label(root, text="", font=self.normalFont)
        self.answerLkneeSS.pack()
        self.answerLkneeSS.place(x=1275, y=100, anchor=NE)

        self.labelLelbowSS = Label(root, text="Left Arm Angle at 2nd to Last Step", font=self.normalFont)
        self.labelLelbowSS.pack()
        self.labelLelbowSS.place(x=1000, y=130, anchor=NW)

        self.answerLelbowSS = Label(root, text="", font=self.normalFont)
        self.answerLelbowSS.pack()
        self.answerLelbowSS.place(x=1275, y=130, anchor=NE)

        self.labelBackSS = Label(root, text="Back Angle at 2nd to Last Step:", font=self.normalFont)
        self.labelBackSS.pack()
        self.labelBackSS.place(x=1000, y=160, anchor=NW)

        self.answerBackSS = Label(root, text="", font=self.normalFont)
        self.answerBackSS.pack()
        self.answerBackSS.place(x=1275, y=160, anchor=NE)

        self.labelVelocitySS = Label(root, text="Ball Velocity at 2nd to Last Step:", font=self.normalFont)
        self.labelVelocitySS.pack()
        self.labelVelocitySS.place(x=1000, y=190, anchor=NW)

        self.answerVelocitySS = Label(root, text="", font=self.normalFont)
        self.answerVelocitySS.pack()
        self.answerVelocitySS.place(x=1275, y=190, anchor=NE)

def cosineLaw(a,mid,c):

    # (mid^2) = (a^2)+(c^2)-(2*a*c)*cos(midAngle)
    midAngle = acos(((mid**2)-(a**2)-(c**2))/(-2*a*c))
    midAngle = midAngle * 180 / math.pi
    return midAngle

def pythag(x1,x2,y1,y2):
    distance = sqrt(pow((x1-x2),2)+pow((y1-y2),2))
    return distance

def pythagAngle(x1,x2,y1,y2):

    angle  = tan(abs(y1-y2)/abs(x1-x2))
    angle = angle * 180 / math.pi
    return angle

def checkPerson(jsonData,width):

    try:
        personNum = None
        peopleArray = []
        roughX = None
        middle = width/2

        if len(jsonData["people"]) == 1:
            personNum = 0
        else:
            for i in range(0,len(jsonData["people"])):
                if jsonData["people"][i]["pose_keypoints_2d"][36] > 0:
                    roughX = jsonData["people"][i]["pose_keypoints_2d"][36]
                elif jsonData["people"][i]["pose_keypoints_2d"][3] > 0:
                    roughX = jsonData["people"][i]["pose_keypoints_2d"][3]
                elif jsonData["people"][i]["pose_keypoints_2d"][6] > 0:
                    roughX = jsonData["people"][i]["pose_keypoints_2d"][6]
                else:
                    roughX = 0
                peopleArray.append(abs(roughX - middle))

            personNum = numpy.argmin(peopleArray)
    except:
        personNum = 0

    return personNum

def trackingAlgo(jsonNew,jsonOld,personNum,lastFramePerson):
    #jsonNew["people"][0]["pose_keypoints_2d"][0]
    try:
        #Legs
        rr = pythag(jsonNew["people"][personNum]["pose_keypoints_2d"][30],jsonOld["people"][lastFramePerson]["pose_keypoints_2d"][30],jsonNew["people"][personNum]["pose_keypoints_2d"][31],jsonOld["people"][lastFramePerson]["pose_keypoints_2d"][31])
        rl = pythag(jsonNew["people"][personNum]["pose_keypoints_2d"][30],jsonOld["people"][lastFramePerson]["pose_keypoints_2d"][39],jsonNew["people"][personNum]["pose_keypoints_2d"][31],jsonOld["people"][lastFramePerson]["pose_keypoints_2d"][39])
        if rr > rl:
            rhipx = jsonNew["people"][personNum]["pose_keypoints_2d"][27]
            rhipy = jsonNew["people"][personNum]["pose_keypoints_2d"][28]
            rhipc = jsonNew["people"][personNum]["pose_keypoints_2d"][29]
            rkneex = jsonNew["people"][personNum]["pose_keypoints_2d"][30]
            rkneey = jsonNew["people"][personNum]["pose_keypoints_2d"][31]
            rkneec = jsonNew["people"][personNum]["pose_keypoints_2d"][32]
            ranklex = jsonNew["people"][personNum]["pose_keypoints_2d"][33]
            rankley = jsonNew["people"][personNum]["pose_keypoints_2d"][34]
            ranklec = jsonNew["people"][personNum]["pose_keypoints_2d"][35]
            rbigtoex = jsonNew["people"][personNum]["pose_keypoints_2d"][66]
            rbigtoey = jsonNew["people"][personNum]["pose_keypoints_2d"][67]
            rbigtoec = jsonNew["people"][personNum]["pose_keypoints_2d"][68]
            rsmalltoex = jsonNew["people"][personNum]["pose_keypoints_2d"][69]
            rsmalltoey = jsonNew["people"][personNum]["pose_keypoints_2d"][70]
            rsmalltoec = jsonNew["people"][personNum]["pose_keypoints_2d"][71]
            rheelx = jsonNew["people"][personNum]["pose_keypoints_2d"][72]
            rheely = jsonNew["people"][personNum]["pose_keypoints_2d"][73]
            rheelc = jsonNew["people"][personNum]["pose_keypoints_2d"][74]

            jsonNew["people"][personNum]["pose_keypoints_2d"][27] = jsonNew["people"][personNum]["pose_keypoints_2d"][36]
            jsonNew["people"][personNum]["pose_keypoints_2d"][28] = jsonNew["people"][personNum]["pose_keypoints_2d"][37]
            jsonNew["people"][personNum]["pose_keypoints_2d"][29] = jsonNew["people"][personNum]["pose_keypoints_2d"][38]
            jsonNew["people"][personNum]["pose_keypoints_2d"][30] = jsonNew["people"][personNum]["pose_keypoints_2d"][39]
            jsonNew["people"][personNum]["pose_keypoints_2d"][31] = jsonNew["people"][personNum]["pose_keypoints_2d"][40]
            jsonNew["people"][personNum]["pose_keypoints_2d"][32] = jsonNew["people"][personNum]["pose_keypoints_2d"][41]
            jsonNew["people"][personNum]["pose_keypoints_2d"][33] = jsonNew["people"][personNum]["pose_keypoints_2d"][42]
            jsonNew["people"][personNum]["pose_keypoints_2d"][34] = jsonNew["people"][personNum]["pose_keypoints_2d"][43]
            jsonNew["people"][personNum]["pose_keypoints_2d"][35] = jsonNew["people"][personNum]["pose_keypoints_2d"][44]
            jsonNew["people"][personNum]["pose_keypoints_2d"][66] = jsonNew["people"][personNum]["pose_keypoints_2d"][57]
            jsonNew["people"][personNum]["pose_keypoints_2d"][67] = jsonNew["people"][personNum]["pose_keypoints_2d"][58]
            jsonNew["people"][personNum]["pose_keypoints_2d"][68] = jsonNew["people"][personNum]["pose_keypoints_2d"][59]
            jsonNew["people"][personNum]["pose_keypoints_2d"][69] = jsonNew["people"][personNum]["pose_keypoints_2d"][60]
            jsonNew["people"][personNum]["pose_keypoints_2d"][70] = jsonNew["people"][personNum]["pose_keypoints_2d"][61]
            jsonNew["people"][personNum]["pose_keypoints_2d"][71] = jsonNew["people"][personNum]["pose_keypoints_2d"][62]
            jsonNew["people"][personNum]["pose_keypoints_2d"][72] = jsonNew["people"][personNum]["pose_keypoints_2d"][63]
            jsonNew["people"][personNum]["pose_keypoints_2d"][73] = jsonNew["people"][personNum]["pose_keypoints_2d"][64]
            jsonNew["people"][personNum]["pose_keypoints_2d"][74] = jsonNew["people"][personNum]["pose_keypoints_2d"][65]

            jsonNew["people"][personNum]["pose_keypoints_2d"][36] = rhipx
            jsonNew["people"][personNum]["pose_keypoints_2d"][37] = rhipy
            jsonNew["people"][personNum]["pose_keypoints_2d"][38] = rhipc
            jsonNew["people"][personNum]["pose_keypoints_2d"][39] = rkneex
            jsonNew["people"][personNum]["pose_keypoints_2d"][40] = rkneey
            jsonNew["people"][personNum]["pose_keypoints_2d"][41] = rkneec
            jsonNew["people"][personNum]["pose_keypoints_2d"][42] = ranklex
            jsonNew["people"][personNum]["pose_keypoints_2d"][43] = rankley
            jsonNew["people"][personNum]["pose_keypoints_2d"][44] = ranklec
            jsonNew["people"][personNum]["pose_keypoints_2d"][57] = rbigtoex
            jsonNew["people"][personNum]["pose_keypoints_2d"][58] = rbigtoey
            jsonNew["people"][personNum]["pose_keypoints_2d"][59] = rbigtoec
            jsonNew["people"][personNum]["pose_keypoints_2d"][60] = rsmalltoex
            jsonNew["people"][personNum]["pose_keypoints_2d"][61] = rsmalltoey
            jsonNew["people"][personNum]["pose_keypoints_2d"][62] = rsmalltoec
            jsonNew["people"][personNum]["pose_keypoints_2d"][63] = rheelx
            jsonNew["people"][personNum]["pose_keypoints_2d"][64] = rheely
            jsonNew["people"][personNum]["pose_keypoints_2d"][65] = rheelc
    except:
        return jsonNew

    return jsonNew

def analyzeFrame(jsonData,analysisNum,personNum):


    rTibia = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][33],
                    jsonData["people"][personNum]["pose_keypoints_2d"][30],
                    jsonData["people"][personNum]["pose_keypoints_2d"][34],
                    jsonData["people"][personNum]["pose_keypoints_2d"][31])
    rFemur = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][30],
                    jsonData["people"][personNum]["pose_keypoints_2d"][27],
                    jsonData["people"][personNum]["pose_keypoints_2d"][31],
                    jsonData["people"][personNum]["pose_keypoints_2d"][28])
    mid = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][33],
                 jsonData["people"][personNum]["pose_keypoints_2d"][27],
                 jsonData["people"][personNum]["pose_keypoints_2d"][34],
                 jsonData["people"][personNum]["pose_keypoints_2d"][28])

    rkneeAngle = cosineLaw(rTibia, mid, rFemur)

    rHumerus = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][6],
                      jsonData["people"][personNum]["pose_keypoints_2d"][9],
                      jsonData["people"][personNum]["pose_keypoints_2d"][7],
                      jsonData["people"][personNum]["pose_keypoints_2d"][10])
    rRadius = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][9],
                     jsonData["people"][personNum]["pose_keypoints_2d"][12],
                     jsonData["people"][personNum]["pose_keypoints_2d"][10],
                     jsonData["people"][personNum]["pose_keypoints_2d"][13])
    mid = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][6],
                 jsonData["people"][personNum]["pose_keypoints_2d"][12],
                 jsonData["people"][personNum]["pose_keypoints_2d"][7],
                 jsonData["people"][personNum]["pose_keypoints_2d"][13])

    relbowAngle = cosineLaw(rHumerus, mid, rRadius)

    lTibia = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][42],
                    jsonData["people"][personNum]["pose_keypoints_2d"][39],
                    jsonData["people"][personNum]["pose_keypoints_2d"][43],
                    jsonData["people"][personNum]["pose_keypoints_2d"][40])
    lFemur = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][39],
                    jsonData["people"][personNum]["pose_keypoints_2d"][36],
                    jsonData["people"][personNum]["pose_keypoints_2d"][40],
                    jsonData["people"][personNum]["pose_keypoints_2d"][37])
    mid = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][42],
                 jsonData["people"][personNum]["pose_keypoints_2d"][36],
                 jsonData["people"][personNum]["pose_keypoints_2d"][43],
                 jsonData["people"][personNum]["pose_keypoints_2d"][37])

    lkneeAngle = cosineLaw(lTibia, mid, lFemur)

    lHumerus = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][15],
                      jsonData["people"][personNum]["pose_keypoints_2d"][18],
                      jsonData["people"][personNum]["pose_keypoints_2d"][16],
                      jsonData["people"][personNum]["pose_keypoints_2d"][19])
    lRadius = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][18],
                     jsonData["people"][personNum]["pose_keypoints_2d"][21],
                     jsonData["people"][personNum]["pose_keypoints_2d"][19],
                     jsonData["people"][personNum]["pose_keypoints_2d"][22])
    mid = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][15],
                 jsonData["people"][personNum]["pose_keypoints_2d"][21],
                 jsonData["people"][personNum]["pose_keypoints_2d"][16],
                 jsonData["people"][personNum]["pose_keypoints_2d"][22])

    lelbowAngle = cosineLaw(lHumerus, mid, lRadius)

    imaginaryX = abs(
        jsonData["people"][personNum]["pose_keypoints_2d"][3] - jsonData["people"][personNum]["pose_keypoints_2d"][24])
    imaginaryY = abs(
        jsonData["people"][personNum]["pose_keypoints_2d"][4] - jsonData["people"][personNum]["pose_keypoints_2d"][25])
    back = pythag(jsonData["people"][personNum]["pose_keypoints_2d"][3],
                  jsonData["people"][personNum]["pose_keypoints_2d"][24],
                  jsonData["people"][personNum]["pose_keypoints_2d"][4],
                  jsonData["people"][personNum]["pose_keypoints_2d"][25])

    backAngle = cosineLaw(imaginaryX, imaginaryY, back)

    rkneeAngle = "{0:.2f}".format(rkneeAngle)
    relbowAngle = "{0:.2f}".format(relbowAngle)
    lkneeAngle = "{0:.2f}".format(lkneeAngle)
    lelbowAngle = "{0:.2f}".format(lelbowAngle)
    backAngle = "{0:.2f}".format(backAngle)

    if analysisNum == 1:
        app.answerRknee.config(text=rkneeAngle)
        app.answerRelbow.config(text=relbowAngle)
        app.answerLknee.config(text=lkneeAngle)
        app.answerLelbow.config(text=lelbowAngle)
        app.answerBack.config(text=backAngle)
    elif analysisNum ==2:
        app.answerRkneeLS.config(text=rkneeAngle)
        app.answerRelbowLS.config(text=relbowAngle)
        app.answerLkneeLS.config(text=lkneeAngle)
        app.answerLelbowLS.config(text=lelbowAngle)
        app.answerBackLS.config(text=backAngle)
    elif analysisNum == 3:
        app.answerRkneeSS.config(text=rkneeAngle)
        app.answerRelbowSS.config(text=relbowAngle)
        app.answerLkneeSS.config(text=lkneeAngle)
        app.answerLelbowSS.config(text=lelbowAngle)
        app.answerBackSS.config(text=backAngle)

def selectFile():
    file = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
    ("All Files", "*.*"), ("MOV files", "*.MOV"), ("MP4 files", "*.mp4"), ("AVI files", "*.avi")))
    app.fileBox.insert(END, file)

def playVideo():  # Creates the threads where the videos are played

    thread = None
    thread2 = None

    if app.startButton.cget("text") == "Start":

        global mainFile
        global fileName
        global directory
        global video
        global video2

        mainFile = app.fileBox.get("1.0", 'end-1c')
        fileName = os.path.basename(mainFile)
        directory = os.path.splitext(mainFile)[0]

        newClip = VideoFileClip(mainFile)
        newFile = moviepy.video.fx.all.gamma_corr(newClip, .5)
        newFile = moviepy.video.fx.all.lum_contrast(newFile,0,1,.15)
        newFile.write_videofile(directory + "_Processed" + ".mp4")

        if not os.path.exists(directory):
            os.makedirs(directory)

        # openPose = r"C:\Users\okeefel\Documents\openpose-1.4.0-win64-gpu-binaries\bin\OpenPoseDemo.exe"
        openPose = r"bin\OpenPoseDemo.exe"
        fileFlag = r" --video " + directory + "_Processed" + ".mp4" #unprocessed file to run
        dataFlag = r" --write_json " + directory #where it saves the raw data
        videoFlag = r" --write_video " + directory + "_Processed" + ".MOV"
        # framesFlag = r" --frame_step " + app.framesBox.get("1.0", 'end-1c')#skips however many frames
        displayFlag = r" --display 0" #Will not run on screen
        peopleFlag = r" --number_people_max 1"
        # trackingFlag = r" --tracking 0"
        scaleFlag = r" --keypoint_scale 0"

        os.chdir(r"C:\Users\okeefel\Documents\openpose-1.4.0-win64-gpu-binaries")
        os.system(openPose + fileFlag + dataFlag + videoFlag + displayFlag + peopleFlag + scaleFlag)

        video = imageio.get_reader(mainFile)
        video2 = imageio.get_reader(directory + "_Processed" + ".MOV")

        vid = cv2.VideoCapture(mainFile)  #used to capture width
        height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

        videoLabel = tk.Label()
        videoLabel.pack()
        videoLabel.place(x=20, y=300, anchor=NW)
        thread = threading.Thread(target=stream, args=(videoLabel,))
        thread.daemon = 1
        thread.start()
        videoLabel2 = tk.Label()
        videoLabel2.pack()
        videoLabel2.place(x=520, y=300, anchor=NW)
        thread2 = threading.Thread(target=stream2, args=(videoLabel2,))
        thread2.daemon = 1
        thread2.start()

        #Parse through all data

        lastFrame = None
        velocityFrame = None #Beggining of where velocity is measured from
        fileCount = 0

        for file in os.listdir(directory): #file will be the json files
            if file.endswith(".json"):
                fileCount = fileCount + 1

        lastFrame = None  # frame before the current one being analyzed
        badFrames = 0  # number of bad frames between good ones
        lastfootLangle = None
        lastfootRangle = None
        lastFramePerson = None
        personNum =None
        step = 1
        skipFrame = 0

        shoeNumber = app.boxShoe.get("1.0", 'end-1c')
        if shoeNumber == 6:
            shoeLength = 9.3125
        elif shoeNumber == 6.5:
            shoeLength = 9.5
        elif shoeNumber == 7:
            shoeLength = 9.6875
        elif shoeNumber == 7.5:
            shoeLength = 9.8125
        elif shoeNumber == 8:
            shoeLength = 10
        elif shoeNumber == 8.5:
            shoeLength = 10.1875
        elif shoeNumber == 9:
            shoeLength = 10.3125
        elif shoeNumber == 9.5:
            shoeLength = 10.5
        elif shoeNumber == 10:
            shoeLength = 10.6875
        elif shoeNumber == 10.5:
            shoeLength = 10.8125
        elif shoeNumber == 11:
            shoeLength = 11
        elif shoeNumber == 11.5:
            shoeLength = 11.1875
        elif shoeNumber == 12:
            shoeLength = 11.3125
        elif shoeNumber == 12.5:
            shoeLength = 11.5
        elif shoeNumber == 13:
            shoeLength = 11.6875
        elif shoeNumber == 13.5:
            shoeLength = 11.8125
        elif shoeNumber == 14:
            shoeLength = 12
        elif shoeNumber == 14.5:
            shoeLength = 12.1875
        elif shoeNumber == 15:
            shoeLength = 12.3125
        else:
            shoeLength = 10.6875  # average shoe size if left blank

        for fileNum in range(fileCount,0,-1): #file will be the json files
            jsonName = None
            if fileNum <= 10 :
                fileNum = fileNum-1
                fileNum = str(fileNum)
                jsonName = directory + r"/" + os.path.splitext(fileName)[0] + "_Processed_00000000000" + fileNum + "_keypoints.json"
            elif fileNum > 10 and fileNum <= 100:
                fileNum = fileNum - 1
                fileNum = str(fileNum)
                jsonName = directory + r"/" + os.path.splitext(fileName)[0] + "_Processed_0000000000" + fileNum + "_keypoints.json"
            elif fileNum > 100:
                fileNum = fileNum - 1
                fileNum = str(fileNum)
                jsonName = directory + r"/" + os.path.splitext(fileName)[0] + "_Processed_000000000" + fileNum + "_keypoints.json"

            with open(jsonName) as handle:
                jsonData = json.loads(handle.read())

                personNum = checkPerson(jsonData,width)

                #236 to 237 on jonathans frames to test
                if (lastFrame != None) & (skipFrame != 1): #Check all of the important points against previous points as an attempt at tracking
                    jsonData = trackingAlgo(jsonData,lastFrame,personNum,lastFramePerson)

                #fill arrays then save graph
                try:
                    x_list = [jsonData["people"][personNum]["pose_keypoints_2d"][0], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][3], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][6], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][9], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][12], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][15], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][18], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][21], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][24], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][27], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][30], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][33], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][36], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][39], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][42], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][45], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][48], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][51], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][54], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][57], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][60], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][63], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][66], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][69], \
                              jsonData["people"][personNum]["pose_keypoints_2d"][72], \
                                ]
                    y_list = [jsonData["people"][personNum]["pose_keypoints_2d"][1]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][4]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][7]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][10]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][13]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][16]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][19]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][22]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][25]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][28]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][31]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][34]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][37]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][40]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][43]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][46]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][49]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][52]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][55]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][58]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][61]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][64]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][67]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][70]*-1+1000, \
                              jsonData["people"][personNum]["pose_keypoints_2d"][73]*-1+1000, \
                              ]
                    words = ["nose", \
                             "neck", \
                             "Rshoulder", \
                             "Relbow", \
                             "Rwrist", \
                             "Lshoulder", \
                             "Lelbow", \
                             "Lwrist", \
                             "Midhip", \
                             "Rhip", \
                             "Rknee", \
                             "Rankle", \
                             "Lhip", \
                             "Lknee", \
                             "Lankle", \
                             "Reye", \
                             "Leye", \
                             "Rear", \
                             "Lear", \
                             "LBigtoe", \
                             "LSmalltoe", \
                             "Lheel", \
                             "Rbigtoe", \
                             "Rsmalltoe", \
                             "Rheel", \
                              ]

                    fig, ax = matplotlib.pyplot.subplots()
                    ax.scatter(x_list,y_list)

                    for i, txt in enumerate(words):
                        ax.annotate(txt,(x_list[i],y_list[i]))

                    matplotlib.pyplot.axis([numpy.amin(x_list)-.1,numpy.amax(x_list)+.1,numpy.amin(y_list)-.1,numpy.amax(y_list)-.3])
                    fig.savefig(directory + r"/" + os.path.splitext(fileName)[0] + "_Processed_000" + fileNum + ".png")
                except:
                    badFrames = badFrames+1

                skipFrame = 0

                try:
                    if jsonData["people"][personNum]["pose_keypoints_2d"][59] >= .2 :
                        footLfrontX = jsonData["people"][personNum]["pose_keypoints_2d"][57]
                        footLfrontY = jsonData["people"][personNum]["pose_keypoints_2d"][58]
                    elif jsonData["people"][0]["pose_keypoints_2d"][62] >= .2 :
                        footLfrontX = jsonData["people"][personNum]["pose_keypoints_2d"][60]
                        footLfrontY= jsonData["people"][personNum]["pose_keypoints_2d"][61]
                    else:
                        skipFrame = 1

                    if jsonData["people"][personNum]["pose_keypoints_2d"][65] >= .2 :
                        footLrearX = jsonData["people"][personNum]["pose_keypoints_2d"][63]
                        footLrearY = jsonData["people"][personNum]["pose_keypoints_2d"][64]
                    elif jsonData["people"][personNum]["pose_keypoints_2d"][44] >= .2 :
                        footLrearX = jsonData["people"][personNum]["pose_keypoints_2d"][42]
                        footLrearY= jsonData["people"][personNum]["pose_keypoints_2d"][43]
                    else:
                        skipFrame = 1
                except:
                    skipFrame = 1

                try:
                    if jsonData["people"][personNum]["pose_keypoints_2d"][68] >= .2 :
                        footRfrontX = jsonData["people"][personNum]["pose_keypoints_2d"][66]
                        footRfrontY = jsonData["people"][personNum]["pose_keypoints_2d"][67]
                    elif jsonData["people"][0]["pose_keypoints_2d"][71] >= .2 :
                        footRfrontX = jsonData["people"][personNum]["pose_keypoints_2d"][69]
                        footRfrontY= jsonData["people"][personNum]["pose_keypoints_2d"][70]
                    else:
                        skipFrame = 1

                    if jsonData["people"][personNum]["pose_keypoints_2d"][74] >= .2 :
                        footRrearX = jsonData["people"][personNum]["pose_keypoints_2d"][72]
                        footRrearY = jsonData["people"][personNum]["pose_keypoints_2d"][73]
                    elif jsonData["people"][personNum]["pose_keypoints_2d"][35] >= .2 :
                        footRrearX = jsonData["people"][personNum]["pose_keypoints_2d"][33]
                        footRrearY= jsonData["people"][personNum]["pose_keypoints_2d"][34]
                    else:
                        skipFrame = 1
                except:
                    skipFrame = 1


                if fileNum == str(fileCount-1): #The first frame starts with when ball is being released
                    analyzeFrame(jsonData,1,personNum)
                    velocityFrame = jsonData
                elif fileNum == str(fileCount-4): #Finds ball velocity using first and second frame

                    footL = pythag(footLfrontX, footLrearX, footLfrontY, footLrearY)
                    wristDistance = pythag(velocityFrame["people"][personNum]["pose_keypoints_2d"][12], jsonData["people"][personNum]["pose_keypoints_2d"][12], \
                                           velocityFrame["people"][personNum]["pose_keypoints_2d"][13], jsonData["people"][personNum]["pose_keypoints_2d"][13])

                    distanceInches = shoeLength * .85 * wristDistance / footL
                    distanceMiles = distanceInches / 63360
                    timeHours = (1 / 239.98) * (1 / 3600)
                    ballVelocity = distanceMiles / timeHours
                    ballVelocity = round(ballVelocity,2)
                    app.answerVelocity.config(text=ballVelocity)

                if skipFrame == 0 :
                    imaginaryX = abs(footLfrontX - footLrearX)
                    imaginaryY = abs(footLfrontY - footLrearY)
                    footL = pythag(footLfrontX,footLrearX,footLfrontY,footLrearY)
                    footLangle = cosineLaw(imaginaryX, imaginaryY, footL)

                    imaginaryX = abs(footRfrontX - footRrearX)
                    imaginaryY = abs(footRfrontY - footRrearY)
                    footR = pythag(footRfrontX, footRrearX, footRfrontY, footRrearY)
                    footRangle = cosineLaw(imaginaryX, imaginaryY, footR)

                    if (step == 1) & (fileNum != str(fileCount-1)):
                        if footLangle > lastfootLangle+8:
                            analyzeFrame(lastFrame,2,lastFramePerson)
                            step = step + 1
                            print(jsonName)

                    if (step == 2) & (fileNum != str(fileCount-1)): #Second to last step
                        if jsonData["people"][personNum]["pose_keypoints_2d"][30] > jsonData["people"][personNum]["pose_keypoints_2d"][39]:
                            if footRangle > 20:
                                analyzeFrame(lastFrame,3,lastFramePerson)
                                step = step + 1
                                print(jsonName)

                    lastfootLangle = footLangle
                    lastfootRangle = footRangle

                lastFrame = jsonData
                lastFramePerson = personNum

                # lastfootRrearX = footRrearX
                # lastfootRrearY = footRrearY
                # lastfootRfrontX = footRfrontX
                # lastfootRfrontY = footRfrontY
                #
                # lastfootLrearX = footLrearX
                # lastfootLrearY = footLrearY
                # lastfootLfrontX = footLfrontX
                # lastfootLfrontY = footLfrontY

        data = {}

        data['Info'] = []
        data['Info'].append({
            'Name': app.boxName.get("1.0", 'end-1c'),
            'Gender': app.genderMF.get(),
            'Age': app.boxAge.get("1.0", 'end-1c'),
            'Feet': app.boxFeet.get("1.0", 'end-1c'),
            'Inches': app.boxInches.get("1.0", 'end-1c'),
            'Shoe Size': app.boxShoe.get("1.0", 'end-1c'),
        })
        data['Release'] = []
        data['Release'].append({
            'Right Leg Angle' : app.answerRknee.cget("text"),
            'Left Leg Angle': app.answerLknee.cget("text"),
            'Right Arm Angle': app.answerRelbow.cget("text"),
            'Left Arm Angle': app.answerLelbow.cget("text"),
            'Back Angle': app.answerBack.cget("text"),
            'Ball Velocity': app.answerVelocity.cget("text"),
        })
        data['Last Step'] = []
        data['Last Step'].append({
            'Right Leg Angle': app.answerRkneeLS.cget("text"),
            'Left Leg Angle': app.answerLkneeLS.cget("text"),
            'Right Arm Angle': app.answerRelbowLS.cget("text"),
            'Left Arm Angle': app.answerLelbowLS.cget("text"),
            'Back Angle': app.answerBackLS.cget("text"),
        })
        data['2nd to Last Step'] = []
        data['2nd to Last Step'].append({
            'Right Leg Angle': app.answerRkneeSS.cget("text"),
            'Left Leg Angle': app.answerLkneeSS.cget("text"),
            'Right Arm Angle': app.answerRelbowSS.cget("text"),
            'Left Arm Angle': app.answerLelbowSS.cget("text"),
            'Back Angle': app.answerBackSS.cget("text"),
        })

        with open(directory + '.txt', 'w') as outfile:
                json.dump(data,outfile)

        os.remove(directory + "_Processed" + ".mp4")
        app.startButton.config(text="Pause")
    elif app.startButton.cget("text") == "Pause":
        app.startButton.config(text="Continue")
    elif app.startButton.cget("text") == "Continue":
        app.startButton.config(text="Pause")

def restartVideo():
    app.startButton.config(text="Start")
    playVideo()

def stream(label):  # First Video

    for image in video.iter_data():
        while app.startButton.cget("text") == "Continue":
            sleep(1)
        img = Image.fromarray(image)
        img2 = img.resize((500, 500), Image.ANTIALIAS)
        img3 = ImageTk.PhotoImage(img2)
        label.config(image=img3)
        label.image = img3

def stream2(label):  # Second Video

    for image in video2.iter_data():
        while app.startButton.cget("text") == "Continue":
            sleep(1)

        img = Image.fromarray(image)
        img2 = img.resize((500, 500), Image.ANTIALIAS)
        img3 = ImageTk.PhotoImage(img2)
        label.config(image=img3)
        label.image = img3

root = tk.Tk()
root.state('zoomed')
app = Application(master=root)
app.mainloop()
