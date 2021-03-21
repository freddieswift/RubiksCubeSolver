import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import imageProcessing
from twophase.solve import Solver
import socket

class Face():
		#Class to represent a face of the cube
		#9 rectangles are drawn on the screen for each face
		#and stored in a list so the colour of the squares can be accessed
	def __init__(self, canvas, start_x, start_y, size, colour):
		self.squares = []
		self.canvas=canvas
		buffer = size+2

		self.squares.append(Square(canvas,start_x,start_y,size,"gray",False))
		self.squares.append(Square(canvas,start_x+buffer,start_y,size,"gray",False))
		self.squares.append(Square(canvas,start_x+(buffer * 2),start_y,size,"gray",False))

		self.squares.append(Square(canvas,start_x,start_y+buffer,size,"gray",False))
		self.squares.append(Square(canvas,start_x+buffer,start_y+buffer,size,colour,True))
		self.squares.append(Square(canvas,start_x+(buffer*2),start_y+buffer,size,"gray",False))

		self.squares.append(Square(canvas,start_x,start_y+(buffer*2),size,"gray",False))
		self.squares.append(Square(canvas,start_x+buffer,start_y+(buffer*2),size,"gray",False))
		self.squares.append(Square(canvas,start_x+(buffer*2),start_y+(buffer*2),size,"gray",False))

	
	# function to set the colours of the sqaures on the face
	# takes the list of colours as captured by the camera, loops through it, and sets the
	# colour of the sqaure accordingly
	def setColours(self, colourList):
		for i, square in enumerate(self.squares):
			if (colourList[i] == "W"):
				self.canvas.itemconfigure(self.squares[i].id, fill="white")
			elif (colourList[i] == "Y"):
				self.canvas.itemconfigure(self.squares[i].id, fill="yellow2")
			elif (colourList[i] == "B"):
				self.canvas.itemconfigure(self.squares[i].id, fill="blue")
			elif (colourList[i] == "G"):
				self.canvas.itemconfigure(self.squares[i].id, fill="green")
			elif (colourList[i] == "R"):
				self.canvas.itemconfigure(self.squares[i].id, fill="red")
			elif (colourList[i] == "O"):
				self.canvas.itemconfigure(self.squares[i].id, fill="orange2")


	# loops though the list of squares of the face and adds the associated face symbol
	# to a string
	# The solver needs the cube to be in the format "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
	# where the white face id UP(U), red face is FRONT(F), blue face is RIGHT(R)
	# cube must be oriented in this way when applying the solution
	def getColours(self):
		colourString=[]
		for i in range(len(self.squares)):
			if self.canvas.itemcget(self.squares[i].id, "fill") == "white":
				colourString.append("U")
			elif self.canvas.itemcget(self.squares[i].id, "fill") == "yellow2":
				colourString.append("D")
			elif self.canvas.itemcget(self.squares[i].id, "fill") == "blue":
				colourString.append("R")
			elif self.canvas.itemcget(self.squares[i].id, "fill") == "green":
				colourString.append("L")
			elif self.canvas.itemcget(self.squares[i].id, "fill") == "orange2":
				colourString.append("B")
			elif self.canvas.itemcget(self.squares[i].id, "fill") == "red":
				colourString.append("F")
			elif self.canvas.itemcget(self.squares[i].id, "fill") == "gray":
				colourString.append("Unknown")
		return ''.join(colourString)


#class to represent the squares of each face
class Square():
	# canvas = canvas to be drawn on
	# x = x start postion
	# y = y start position
	# size = size of square in pixels
	# colour = colour of square to be set
	# centrePeice = whether sqaure can change colour - centre peices cannot change colour
	def __init__(self, canvas, x, y, size, colour, centrePeice):
		self.centrePeice = centrePeice
		self.canvas = canvas
		# draw rectangle at specified place and size
		self.id = self.canvas.create_rectangle((x,y,x+size,y+size), fill=colour)
		# add click event so user can click each sqaure to change it's colour
		self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.set_colour)


	#sets the colour of the square, check for poisiton of colour in list,
	#the sets the colour as the next on in the list
	#if yellow, sets back to gray
	def set_colour(self, event=None):
		if (self.centrePeice==False):
			colours = ["gray","white","blue","green","red","orange2","yellow2"]
			index = colours.index(self.canvas.itemcget(self.id, "fill"))
			if ((index + 1) <= (len(colours) - 1)):
				self.canvas.itemconfigure(self.id, fill=colours[index + 1])
			else:
				self.canvas.itemconfigure(self.id, fill=colours[0])

			
class App:
	def __init__(self, window, window_title):
		self.window = window
		window.geometry("1400x500")
		self.window.resizable(False, False)
		self.window.title(window_title)

		#solver object to solve the cube
		self.solver = Solver()

		#canvas to draw video feed and cube
		self.canvas = tkinter.Canvas(window, width=1400, height=400)
		self.canvas.grid(row=0)

		#draw the faces onto the canvas
		self.drawFaces()

		#frame to hold the buttons and text view
		self.frame = tkinter.Frame(window)
		self.frame.grid(row=1,sticky="w")


		#create widgets
		solveButton = tkinter.Button(self.frame, text="Solve", height=5, width=40, command=self.solve)
		solveButton.grid(row=1,column=0)

		exitButton = tkinter.Button(self.frame, text="Exit", height=5, width=40, command=window.quit)
		exitButton.grid(row=1,column=1)

		connectButton = tkinter.Button(self.frame, text="Connect Camera", height=5, width=40, command=self.connect)
		connectButton.grid(row=1,column=2)

		self.textBox = tkinter.Text(self.frame, height=5, width=40, wrap=tkinter.WORD)
		self.textBox.grid(row=1,column=3)

		#check var used to determine oif box is check or not
		self.checkVar = tkinter.IntVar(value=1)
		self.checkButton = tkinter.Checkbutton(self.frame, text="Detect Peices?", variable=self.checkVar)
		self.checkButton.grid(row=1,column=4)

		self.ipTextBox = tkinter.Entry(self.canvas)
		self.ipTextBox.place(x=955,y=380)
		self.ipLabel = tkinter.Label(self.canvas, text="IP Address on IP Webcam:").place(x=810,y=380)
		
		self.window.mainloop()

	def solve(self):
		self.textBox.delete(1.0,tkinter.END)
		#cube has to be in the format "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB" for solved cube
		cubeString = self.whiteFace.getColours() + self.blueFace.getColours() + self.redFace.getColours() + self.yellowFace.getColours() + self.greenFace.getColours() + self.orangeFace.getColours()
		#try to solve and put result in text box
		try:
			self.textBox.insert(tkinter.END, self.solver.solve(cubeString))
		except:
			self.textBox.insert(tkinter.END, "Please ensure cube is configured correctly")


	def connect(self):
			# get ip address of video feed from text box
			videoSource = self.ipTextBox.get()
			# ip address has to be in this formet for connection
			fullVideoSource = "https://" + videoSource + "/video"
			self.textBox.delete(1.0,tkinter.END)
			try:
				self.vid = MyVideoCapture(fullVideoSource)
			except:
				self.textBox.insert(tkinter.END, "Cannot connect to video stream")
			else:
				self.textBox.insert(tkinter.END, "Connected to video stream")
				self.delay=15
				self.update()
				self.window.mainloop()

	#draw faces on screen
	def drawFaces(self):
		self.whiteFace = Face(self.canvas, 950, 50, 30,"white")
		self.greenFace = Face(self.canvas, 845, 155, 30,"green")
		self.redFace = Face(self.canvas, 950, 155, 30,"red")
		self.blueFace = Face(self.canvas, 1055, 155, 30,"blue")
		self.orangeFace = Face(self.canvas, 1160, 155, 30,"orange2")
		self.yellowFace = Face(self.canvas, 950, 260, 30,"yellow2")


	# update screen with video feed and perform image processing on the frame
	def update(self):
		# get frame from video feed
		ret, frame = self.vid.getFrame()
		# check whether the user wants to detects the peices, use check box
		# if box checked:
		if self.checkVar.get() == 1:
			contours = imageProcessing.findContours(frame)
			contours = imageProcessing.sortContours(contours, frame)
			# if 9 peices detected
			if len(contours) == 9:
				frame = imageProcessing.drawContours(contours, frame)
				colourList = imageProcessing.findColours(contours, frame)
				self.updateSquares(colourList)
		if ret:
			self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
			self.canvas.create_image(0,0,image=self.photo, anchor=tkinter.NW)

		self.window.after(self.delay, self.update)

	# takes the list of colours found by the camera, finds the middle peices colour,
	# and updates the appropriate face
	def updateSquares(self, colourList):
		if "U" not in colourList:
			if colourList[4] == "W":
				self.whiteFace.setColours(colourList)
			elif colourList[4] == "Y":
				self.yellowFace.setColours(colourList)
			elif colourList[4] == "B":
				self.blueFace.setColours(colourList)
			elif colourList[4] == "G":
				self.greenFace.setColours(colourList)
			elif colourList[4] == "O":
				self.orangeFace.setColours(colourList)
			elif colourList[4] == "R":
				self.redFace.setColours(colourList)


class MyVideoCapture:
	# try to open video stream from ip address enetered by the user
	def __init__(self, video_source):
		self.vid = cv2.VideoCapture(video_source)
		if not self.vid.isOpened():
			raise ValueError("unable to open video source", video_source)

		self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

	# get frame from the video source
	def getFrame(self):
		if self.vid.isOpened():
			ret, frame = self.vid.read()
			frame = cv2.resize(frame, (800, 400))
			if ret:
				return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
			else:
				return (ret, None)
		else:
			return (ret, None)

	def __del__(self):
		if self.vid.isOpened():
			self.vid.release()

App(tkinter.Tk(), "Rubik's Cube Solver")



