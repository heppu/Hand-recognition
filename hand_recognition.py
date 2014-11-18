import SimpleCV
import math
import datetime
 
try:
	cam = SimpleCV.Camera()
except:
	print "Can't open webcam"
	sys.exit()

display = SimpleCV.Display()
normaldisplay = True

hand_xml_a = SimpleCV.HaarCascade("xml/handa.xml") 	# hand fingers up
hand_xml_b = SimpleCV.HaarCascade("xml/handb.xml") 	# hand fingers left to right
hand_xml_c = SimpleCV.HaarCascade("xml/hands.xml") 	# hand fingers left to right


while display.isNotDone():
 	start = datetime.datetime.now()
	if display.mouseRight:
		normaldisplay = not(normaldisplay)
	
	img = cam.getImage().flipHorizontal()
	masked = img.getSkintoneMask()

	hands = masked.findHaarFeatures(hand_xml_d)

	circe_layer = SimpleCV.DrawingLayer((img.width, img.height))
	percent = 0
	x = 0
	y = 0

	print hands

	if hands:
		x, y = hands[0].coordinates()
		x_out = (x - (img.width/2))/float(img.width/2) * 100 				# x coordinate between -100 and 100
		y_out = (-(y - (img.height/2)))/float(img.height/2) * 100			# y coordinate between -100 and 100
		radius = (hands[0].boundingBox()[2] + hands[0].boundingBox()[3])/4	# radius for circl
		percent = hands[0].area() / float(img.width*img.height) * 100 		# area that hand covers between 0 and 100

		circe_layer.circle(hands[0].coordinates(), radius, color=SimpleCV.Color.BLUE, width=5)
		
		masked.addDrawingLayer(circe_layer)
 		masked.applyLayers()
 		img.addDrawingLayer(circe_layer)
 		img.applyLayers()	

		#print x_out, y_out, percent	

 	time =  (datetime.datetime.now() - start).total_seconds() * 1000
 	print "Image analyzed in %sms" % (time)
	
	if normaldisplay:
		img.show()
	else:
		masked.show()