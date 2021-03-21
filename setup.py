from cx_Freeze import setup, Executable

setup(name = "Rubik's Cube Solver",
	version="1.0",
	description="",
	executables=[Executable("gui.py", targetName="Rubik's Cube Solver")])