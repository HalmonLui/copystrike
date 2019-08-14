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

        self.boxName = Text(root, height=1, width=14)
        self.boxName.pack()
        self.boxName.place(x=95, y=43, anchor=NW)

        genderChoices = ["Male", "Female"]
        genderMF = StringVar(root)
        genderMF.set("Male")
        self.boxGender = OptionMenu(root, genderMF, *genderChoices)
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

def cosineLaw(a,mid,c):

    # (mid^2) = (a^2)+(c^2)-(2*a*c)*cos(midAngle)
    midAngle = acos(((mid**2)-(a**2)-(c**2))/(-2*a*c))
    midAngle = midAngle * 180 / math.pi
    return midAngle

def pythag(x1,x2,y1,y2):
    distance = sqrt(pow((x1-x2),2)+pow((y1-y2),2))
    return distance

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
        scaleFlag = r" --keypoint_scale 3"

        os.chdir(r"C:\Users\okeefel\Documents\openpose-1.4.0-win64-gpu-binaries")
        os.system(openPose + fileFlag + dataFlag + videoFlag + displayFlag + peopleFlag + scaleFlag)

        video = imageio.get_reader(mainFile)
        video2 = imageio.get_reader(directory + "_Processed" + ".MOV")

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

        # for root, dirs, files in os.walk("/mydir"):
        #     for file in files:
        #         if file.endswith(".txt"):
        #             print(os.path.join(root, file))

        #Parse through all data

        lastFrame = None

        fileCount = 0

        for file in os.listdir(directory): #file will be the json files
            if file.endswith(".json"):
                fileCount = fileCount + 1

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

                # jsonData["people"][0]["pose_keypoints_2d"][0]
                #fill arrays then save graph
                x_list = [jsonData["people"][0]["pose_keypoints_2d"][0], \
                          jsonData["people"][0]["pose_keypoints_2d"][3], \
                          jsonData["people"][0]["pose_keypoints_2d"][6], \
                          jsonData["people"][0]["pose_keypoints_2d"][9], \
                          jsonData["people"][0]["pose_keypoints_2d"][12], \
                          jsonData["people"][0]["pose_keypoints_2d"][15], \
                          jsonData["people"][0]["pose_keypoints_2d"][18], \
                          jsonData["people"][0]["pose_keypoints_2d"][21], \
                          jsonData["people"][0]["pose_keypoints_2d"][24], \
                          jsonData["people"][0]["pose_keypoints_2d"][27], \
                          jsonData["people"][0]["pose_keypoints_2d"][30], \
                          jsonData["people"][0]["pose_keypoints_2d"][33], \
                          jsonData["people"][0]["pose_keypoints_2d"][36], \
                          jsonData["people"][0]["pose_keypoints_2d"][39], \
                          jsonData["people"][0]["pose_keypoints_2d"][42], \
                          jsonData["people"][0]["pose_keypoints_2d"][45], \
                          jsonData["people"][0]["pose_keypoints_2d"][48], \
                          jsonData["people"][0]["pose_keypoints_2d"][51], \
                          jsonData["people"][0]["pose_keypoints_2d"][54], \
                          jsonData["people"][0]["pose_keypoints_2d"][57], \
                          jsonData["people"][0]["pose_keypoints_2d"][60], \
                          jsonData["people"][0]["pose_keypoints_2d"][63], \
                          jsonData["people"][0]["pose_keypoints_2d"][66], \
                          jsonData["people"][0]["pose_keypoints_2d"][69], \
                          jsonData["people"][0]["pose_keypoints_2d"][72], \
                            ]
                y_list = [jsonData["people"][0]["pose_keypoints_2d"][1]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][4]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][7]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][10]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][13]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][16]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][19]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][22]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][25]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][28]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][31]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][34]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][37]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][40]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][43]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][46]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][49]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][52]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][55]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][58]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][61]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][64]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][67]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][70]*-1+1000, \
                          jsonData["people"][0]["pose_keypoints_2d"][73]*-1+1000, \
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

                if fileNum == str(fileCount-1): #The first frame starts with when ball is being released
                    jsonData["people"][0]["pose_keypoints_2d"][27] #RhipX
                    jsonData["people"][0]["pose_keypoints_2d"][30] #RkneeX
                    jsonData["people"][0]["pose_keypoints_2d"][33] #RankleX

                    jsonData["people"][0]["pose_keypoints_2d"][28]  #RhipY
                    jsonData["people"][0]["pose_keypoints_2d"][31]  #RkneeY
                    jsonData["people"][0]["pose_keypoints_2d"][34]  #RankleY

                    tibia = pythag(jsonData["people"][0]["pose_keypoints_2d"][33],jsonData["people"][0]["pose_keypoints_2d"][30],jsonData["people"][0]["pose_keypoints_2d"][34],jsonData["people"][0]["pose_keypoints_2d"][31])
                    femur = pythag(jsonData["people"][0]["pose_keypoints_2d"][30],jsonData["people"][0]["pose_keypoints_2d"][27],jsonData["people"][0]["pose_keypoints_2d"][31],jsonData["people"][0]["pose_keypoints_2d"][28])
                    mid = pythag(jsonData["people"][0]["pose_keypoints_2d"][33],jsonData["people"][0]["pose_keypoints_2d"][27],jsonData["people"][0]["pose_keypoints_2d"][34],jsonData["people"][0]["pose_keypoints_2d"][28])

                    rkneeAngle = cosineLaw(tibia,mid,femur)

                    print(tibia)
                    print(femur)
                    print(mid)
                    print(rkneeAngle)

                    lastFrame = jsonData


        # (x,y,confidence)
        # 0 Nose
        # 1 Neck
        # 2 RShoulder
        # 3 RElbow
        # 4 RWrist
        # 5 LShoulder
        # 6 LElbow
        # 7 LWrist
        # 8 MidHip
        # 9 RHip
        # 10 RKnee
        # 11 RAnkle
        # 12 LHip
        # 13 LKnee
        # 14 LAnkle
        # 15 REye
        # 16 LEye
        # 17 REar
        # 18 LEar
        # 19 LBigToe
        # 20 LSmallToe
        # 21 LHeel
        # 22 RBigToe
        # 23 RSmallToe
        # 24 RHeel
        # 25 Background

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
