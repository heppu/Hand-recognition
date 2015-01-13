Hand-recognition
================

Hand recognition is a python script that detects hand from image and calculates its coordinates and area.
To use script you need to install [SimpleCV](https://github.com/sightmachine/simplecv).

Use case
--------

This script was made to read images from AR.Drone 2.0 and send values to control it movements by your hand.

Settings
--------

**WEBCAM=True**
If WEBCAM is set to True script will read images from webcam strem.

**URL=""**
If WEBCAM is set to False and URL is defined script will get images from url.

**WATCH=True**
If WATCH is set to True you will see image and blue circle around hand if one is found.
