#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import everything
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


# In[19]:


# Get video source
#vs = cv2.VideoCapture('./strike_lane/Halmon_X_1a.mp4',0)

# Reads in video, tracks the ball, outputs array of ball points/coordinates 
def analyzeVideo(videoName):
    vs = cv2.VideoCapture(videoName,0)
    print(vs)

    # allow the camera or video file to warm up
    time.sleep(2.0)

    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    #greenLower = (0, 180, 0) 
    #greenUpper = (30, 242, 182)
    greenLower = (6, 242, 61) 
    greenUpper = (40, 255, 200)
    pts = deque(maxlen=64)

    # keep looping
    xTemp = 0 #Initialize variables xTemp and yTemp
    yTemp = 0
    toggleFirst = 0
    while True:
        # grab the current frame
        #frame = vs.read()
        _, frame = vs.read()

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if frame is None:
            break

        (w, h, c) = frame.shape # shape the frame to allow w, h and c to be utilized later on

        # resize the frame, blur it, and convert it to the HSV
        # color space
        #frame = imutils.resize(frame, width=600)
        #frame = cv2.resize(frame,(600, w))
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    #        # only proceed if the radius meets a minimum size
    #        if radius > 1:
    #            # draw the circle and centroid on the frame,
    #            # then update the list of tracked points
    #            cv2.circle(frame, (int(x), int(y)), int(radius),
    #                (0, 255, 255), 2)
    #            cv2.circle(frame, center, 5, (0, 0, 255), -1)


            if toggleFirst == 0: # check if first run
                if radius > 1: # only proceed if the radius meets a minimum size
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    toggleFirst = 1
                    xTemp = center[0]
                    yTemp = center[1]
            else: 
                if radius > 1:# only proceed if the radius meets a minimum size
                    if center[0] < xTemp + 50 and center[1] < yTemp + 50: # only proceed if x and y coordinates are near previous
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame, (int(x), int(y)), int(radius),
                            (0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)
                        xTemp = center[0]
                        yTemp = center[1]                    
                        pts.appendleft(center)


        # update the points queue
        #pts.appendleft(center)

        # loop over the set of tracked points
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
            #thickness = 1
            cv2.line(frame, pts[i - 1], pts[i], (0, 255, 255), thickness)
            #print(pts[i])

        # show the frame to our screen
        #cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

    # Release the video capture
    vs.release()

    # close all windows
    cv2.destroyAllWindows()
    #print(pts)
    return pts


# In[24]:


def visualizeData(pts):
    # Get x and y values for graphing
    xValues = np.array([])
    yValues = np.array([])
    for point in pts:
        xValues = np.append(xValues, point[0])
        yValues = np.append(yValues, point[1])
    print(pts)
    print(xValues)
    print(yValues)

    # Line of best poly fit
    from numpy.polynomial.polynomial import polyfit
    b, m = polyfit(xValues, yValues, 1)
    print("slope: " + str(abs(m)))
    
    # Graph it (this is for our own use only, does not help code. May be nice to show graphs in GUI???)
    import matplotlib.pyplot as plt
    get_ipython().run_line_magic('matplotlib', 'inline')

    plt.plot(xValues, yValues, 'o')
    plt.plot(xValues, b + m * xValues, '-')
    plt.gca().invert_yaxis()
    plt.xlabel("X coordinates")
    plt.ylabel("Y coordinates")
    plt.title("Graph ball coordinates")

    plt.show()
    return(abs(m))


# In[20]:


visualizeData(analyzeVideo('./strike_lane_edited/RX4a.mp4'))


# In[28]:


# Open the output file
text_file = open("StrikeBallSlope.txt", "w")


# Loop through the videos and write outputs to file
for x in range(1,5): # for Ryan's strikes
    name = './strike_lane_edited/RX'+ str(x) + 'a.mp4'
    outName = 'Ryan_X_' + str(x)+'\n'
    print(name)
    print(outName)
    text_file.write(outName)
    text_file.write(str(visualizeData(analyzeVideo(name)))+'\n')

for x in range(1,5): # for Halmon's strikes
    name = './strike_lane_edited/HX'+ str(x) + 'a.mp4'
    outName = 'Halmon_X_' + str(x)+'\n'
    print(name)
    print(outName)
    text_file.write(outName)
    text_file.write(str(visualizeData(analyzeVideo(name)))+'\n')
text_file.close()


# In[30]:


# Open the output file
text_file = open("NotStrikeBallSlope.txt", "w")


# Loop through the videos and write outputs to file
for x in range(1,10): # for Ryan's strikes
    name = './not_strike_lane_edited/RO'+ str(x) + 'a.mp4'
    outName = 'Ryan_O_' + str(x)+'\n'
    print(name)
    print(outName)
    text_file.write(outName)
    text_file.write(str(visualizeData(analyzeVideo(name)))+'\n')

for x in range(1,15): # for Halmon's strikes
    name = './not_strike_lane_edited/HO'+ str(x) + 'a.mp4'
    outName = 'Halmon_O_' + str(x)+'\n'
    print(name)
    print(outName)
    text_file.write(outName)
    text_file.write(str(visualizeData(analyzeVideo(name)))+'\n')
text_file.close()

