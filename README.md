# Copystrike (How to Bowl a Better Game)

Halmon Lui, Ryan Parekh, Logan O'keefe

A senior design project

## Abstract

A team of bowling and coding enthusiasts, we came up with a solution to get the best of both worlds.
An application to record a bowl and compare to bowls where the user has gotten a strike before.
It will then tell the user what angles and positions of their form to change in order to have performed a strike again.

## System

- Pose detection uses OpenPose
- Ball detection uses OpenCV
- Machine Learning uses Scikit-Learn
  ![Image of system diagram](/SystemDiagram.jpg)

## How it works

1. Phone camera records bowler and ball
1. OpenPose is used to track the bowler's form
1. OpenCV is used to track the ball down the lane
1. Scikit-Learn takes the features of both bowler's form and ball to return strikes
1. A decision tree then tells the user how to improve

## How to use it

You must first have these on your system:

- Python3
- Jupyter Notebook
- OpenCV
- OpenPose
- Scikit-learn
- Numpy
- Scipy
- Pandas
- Matplotlib

The three parts of the system are not connected yet so you have to run them separately

1. HSV_Picker.ipynb is used to select the HSV range for the ball you are going to track
1. ball_tracking_final.ipynb is used to track the ball down the lane and output the trajectory
1. driver.py is used to track the form of the bowler and outputs a JSON datafile
1. ML_bowling_code_final.ipynb is used to apply supervised learning model KNN and outputs the suggestion
