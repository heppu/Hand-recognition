Hand-recognition
================

Hand recognition is a python script that detects hand from image and calculates its coordinates and area.
To use script you need to install [SimpleCV](https://github.com/sightmachine/simplecv).


Settings
--------
WEBCAM = True

If WEBCAM is set to True script will read images from webcam strem.

URL = "http://localhost:2700/drone"

If WEBCAM is set to False and URL is defined script will get images from url.

WATCH = True

If WATCH is set to True you will see image and blue circle around hand if one is found.
