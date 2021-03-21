Frederick Swift 17076237

Rubik's Cube Solver

Prerequisites:
	- Android Phone with IP Webcam App installed (https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_GB)

Usage:
	- Ensure computer and phone are connected to the same network
	- Please run "Rubik's Cube Solver" in the build folder
	- Ensure IP Webcam app is running
	- Enter the IPv4 Address show at the bottom of IP Webcam
		- Enter the numerical part e.g. the IPv4 address "http://192.168.0.1:8080" would be entered as "192.168.0.1:8080"
	- Press Connect Camera
	- The middle peices do not change relative to each other
		- Ensure the cube is oriented with the white middle peice as the UP face, the red as the FRONT face, blue as RIGHT etc.
	- Rotate the cube round to capture the faces, ensuring that they stay correctly oriented relative to each other
	- Click on an individual square to change it's colour incase it has been incorrectly identified by the camera
	- The Detect Peices check box can be unchecked to stop the camera detecting the cube
		- This can make it easier to change the individual peices
	- Ensure there are only 9 occurences of each colour
	- When the cube is configured correctly, press the solve button to commence the solve
	- The sequence of moves needed to solve the cube will be displayed in the message box
		- U = one turn of the UP(white) face clockwise
		- U' = one turn of the UP(white) face counter clockwise
		- U2 = two turns of the UP(white) face
		- same format for other colours

Contents of twophase are taken from https://github.com/tcbegley/cube-solver

