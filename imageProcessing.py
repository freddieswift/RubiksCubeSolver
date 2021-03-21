import cv2
import numpy as np
import statistics

#takes an image
#processes it and finds the contours
#returns the list of contours
def findContours(image):
	gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	#brightness and contrast
	alpha = 3
	beta = 70
	bc = cv2.addWeighted(gray, alpha, np.zeros(gray.shape, gray.dtype), 0, beta)
	#blur
	blur = cv2.GaussianBlur(bc, (11,11), 0)
	#laplacian filter
	laplacian = cv2.Laplacian(blur, cv2.CV_8UC1, ksize=7)
	#dilation
	kernel = np.ones((5,5), np.uint8)
	dilated = cv2.dilate(laplacian, kernel, iterations=3)
	#threshold
	thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
	#find contours in image
	(contours, hierachy) = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#for each contour, check if it has 4 sides, and width and height are approx the same
	# only if these are true, then add contour to list of square contours
	squareContours = []
	for cnt in contours:
		#arppoximate the shape of the contour
		approx = cv2.approxPolyDP(cnt, 0.04*cv2.arcLength(cnt, True), True)
		#if contour has 4 sides
		if len(approx) == 4:
			#create bounding rectangle to be able to find coordinated, wisth and height of contour
			x,y,w,h = cv2.boundingRect(cnt)
			#if height and width are approx the same
			aspectRatio = float(w)/h
			if aspectRatio >=0.9 or aspectRatio <= 1.1:
				squareContours.append(cnt)
	#find area of each contour and add to areas list
	areas =[]
	for cnt in squareContours:
		area = cv2.contourArea(cnt)
		areas.append(area)
	#find median value of areas
	areas.sort()
	#if contour's area is close to medain area in areas, add to list of valid contours
	validContours = []
	if not areas:
		pass
	else:
		median = statistics.median(areas)
		for cnt in squareContours:
			#print(cv2.contourArea(cnt))
			if cv2.contourArea(cnt) <= median*1.3 and cv2.contourArea(cnt) >= median*0.7:
				validContours.append(cnt)
	return validContours

def whiteBalance(image):
	result = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
	avg_a = np.average(result[:,:,1])
	avg_b = np.average(result[:,:,2])
	result[:,:,1] = result[:,:,1] - ((avg_a - 128) * (result[:,:,0] / 255.0) * 1.1)
	result[:,:,2] = result[:,:,2] - ((avg_b - 128) * (result[:,:,0] / 255.0) * 1.1)
	result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
	return result


def sortContours(contours, image):
	#find origin of contour then sort contours in order based off this
	#return list of sorted contours
	contours.sort(key=lambda x:getContourPrec(x, image.shape[1]))
	return contours

def getContourPrec(contour, cols):
	#find origin of contour to then be able to sort them
	toleranceFactor = 10
	origin = cv2.boundingRect(contour)
	return ((origin[1] // toleranceFactor) * toleranceFactor) * cols + origin[0]

def drawContours(contours, image):
	# takes a list of contours and an image, draws the contours on the image
	# returns the image
	i = 1
	for cnt in contours:
		cv2.drawContours(image, [cnt], -1, (0,0,255), 2)
		x,y,w,h = cv2.boundingRect(cnt)
		text = 'Peice' + str(i)
		cv2.putText(image, text, (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
		i = i + 1
	return image

def showImage(image):
	cv2.imshow('image', image)


#used for debugging
def printColours(contours, frame):
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	i = 1
	for cnt in contours:
		x,y,w,h = cv2.boundingRect(cnt)
		print('Contour:' + str(i) + 'Average color (hsv): ',np.array(cv2.mean(hsv[y:y+h,x:x+w])).astype(np.uint8))
		i = i + 1
		#cv2.rectangle(hsv,(x,y),(x+w,y+h),(0,255,0),2)

def findColours(contours, frame):
	#returns a list of colours representing the face in the image

	#list to hold the colour characters
	colourList = []
	#convert image to hsv colour space	
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# loops through contours, cuts the contour from the image, and finds the HSV values for that section
	# then determines the colour of the section from these values
	for cnt in contours:
		x,y,w,h = cv2.boundingRect(cnt)
		#find the hsv value for the given square
		hsvValues = np.array(cv2.mean(hsv[y:y+h,x:x+w])).astype(np.uint8)
		hue = hsvValues[0]
		sat = hsvValues[1]
		val = hsvValues[2]

		#blue
		if hue >= 10 and hue < 28:
			if sat < 100:
				colourList.append("W")
			else:
				colourList.append("B")
		#green
		elif hue > 30 and hue < 47:
			if sat < 100:
				colourList.append("W")
			else:
				colourList.append("G")
		#orange and red
		elif hue >= 80 and hue < 110:
			if sat > 200 :
				if val > 220:
					colourList.append("O")
				else:
					colourList.append("R")
			elif sat < 140:
				colourList.append("W")
			else:
				colourList.append("O")

		#yellow and white
		elif hue > 50 and hue < 80:
			if sat >= 130:
				colourList.append("Y")
			elif sat < 130:
				colourList.append("W")
			else:
				colourList.append("U")
		else:
			colourList.append("U")

	return colourList
		
	


	
