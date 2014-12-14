import sys
import time
import SimpleCV
import datetime
import urllib2
import requests
import StringIO
from PIL import Image
from httplib import BadStatusLine

# Change WEBCAM to True if you want to read images from webcam
WEBCAM = False

# If webcam is False define URL where images are fetched
URL = "http://localhost:2700/drone"

# Change to True if you want to see images
WATCH = True

# Post url
POST_URL = "http://localhost:2700/coordinates"

if(WEBCAM==False and len(URL)==0):
	print "Use webcam or define url"
	sys.exit()

# Load HaarCascade files
hand_xml_a = SimpleCV.HaarCascade("xml/handa.xml") 	# hand fingers up
hand_xml_b = SimpleCV.HaarCascade("xml/handb.xml") 	# hand fingers left to right
hand_xml_c = SimpleCV.HaarCascade("xml/hands.xml") 	# hand fingers left to right

i=0

def sendData(x, y, area):
	params = dict(xin=x, yin=y, area=area)
	try:
		r = requests.get(POST_URL, params=params, allow_redirects=True)
		print r.content
	except ConnectionError, e:
		print e


def analyze(img, i):
	start = datetime.datetime.now()
	# Mask skintone from image
	masked = img.getSkintoneMask()

	# Start from previous angle for faster recognition
	if(i!=0):
		masked = masked.rotate(i*90, fixed=False)

	# Check for hand in every direction
	for j in xrange(0, 4):
		hands = masked.findHaarFeatures(hand_xml_b)
		if hands:
			break
		else:
			masked = masked.rotate(90, fixed=False)
			i = i+1
			if(i==4):
				i=0
	
	percent = 0
	x = 0
	y = 0

	if hands:
		# Coordinate transform
		x_in, y_in = hands[0].coordinates()
		if(i==0):
			x = x_in
			y = y_in
		elif(i==1):
			x = img.width - y_in
			y = x_in
		elif(i==2):
			x = img.width - x_in
			y = img.height - y_in
		elif(i==3):
			x = y_in	
			y = img.height - x_in

		# Movement calculation
		x_out = (x - (img.width/2))/float(img.width/2) * 100 				# x coordinate between -100 and 100
		y_out = (-(y - (img.height/2)))/float(img.height/2) * 100			# y coordinate between -100 and 100
		radius = (hands[0].boundingBox()[2] + hands[0].boundingBox()[3])/4	# radius for circl
		percent = hands[0].area() / float(img.width*img.height) * 100 		# area that hand covers between 0 and 100

		# Image Drawing
		if(WATCH):
			circe_layer = SimpleCV.DrawingLayer((img.width, img.height))
			circe_layer.circle((x,y), radius, color=SimpleCV.Color.BLUE, width=5)
			masked.addDrawingLayer(circe_layer)
	 		masked.applyLayers()
	 		img.addDrawingLayer(circe_layer)
	 		img.applyLayers()

		print x_out, y_out, percent
		sendData(x_out, y_out, percent)

 	time =  (datetime.datetime.now() - start).total_seconds() * 1000
 	print "Image analyzed in %sms" % (time)

 	# Display images
 	if(WATCH):
		if normaldisplay:
			img.show()
		else:
			masked.rotate(360-(i*90), fixed=False).show()

	return i


if(WEBCAM):
	#Open webcam
	try:
		cam = SimpleCV.Camera()
	except:
		print "Can't open webcam"
		sys.exit()

	if(WATCH):	
		display = SimpleCV.Display()
		normaldisplay = True
		while display.isNotDone():
			if display.mouseRight:
				normaldisplay = not(normaldisplay)
			# Read image from webcam
			img = cam.getImage().flipHorizontal()
			#analyze image
			i = analyze(img, i)
	else:
		while True:
			# Read image from webcam
			img = cam.getImage().flipHorizontal()
			#analyze image
			i = analyze(img, i)


else:	
	if(WATCH):	
		display = SimpleCV.Display()
		normaldisplay = True
		while display.isNotDone():
			if display.mouseRight:
				normaldisplay = not(normaldisplay)
			# Read imger from url
			try:
				im = urllib2.urlopen(URL).read()
				img = Image.open(StringIO.StringIO(im))
				img = SimpleCV.Image(img)
				#analyze image
				i = analyze(img, i)
			except (urllib2.URLError, BadStatusLine) as e:
				print "error"
				time.sleep(5)

	else:
		while True:
			# Read imger from url
			try:
				im = urllib2.urlopen(URL).read()
				img = Image.open(StringIO.StringIO(im))
				img = SimpleCV.Image(img)
				#analyze image
				i = analyze(img, i)
			except (urllib2.URLError, BadStatusLine) as e:
				print "error"
				time.sleep(5)
