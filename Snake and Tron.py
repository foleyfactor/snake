#==========================================#
#                                          #
# Multiplayer Snake & Tron Games           #
# By: Alex Foley                           #
# Code Written From May 29 - June 15, 2015 #
#                                          #
#==========================================#

#Imports
from tkinter import *
tron = __import__('Tron Game')
snake = __import__('Snake Multiplayer')

#Runs the title screen
def titleScreen():
	global currentScreen, screen, titlePhotoImage, master
	#set the value of the current screen
	currentScreen = 0

	#Create a tkinter instance and canvas
	master = Tk()
	screen = Canvas(master, width=840, height=672)
	screen.pack()
	screen.focus_set()

	#Key binding and room title
	master.bind('<Key>', nextScreen)
	master.wm_title('Snake and Tron')

	#Draws title image
	titlePhoto = PhotoImage(file='./titleScreenPhoto.gif')
	titlePhotoImage = screen.create_image(420, 336, image=titlePhoto, anchor='center')
	screen.mainloop()

#Transitions between title and menu screens
def nextScreen(event):
	global currentScreen
	if currentScreen == 0:
		currentScreen = 1
		choiceScreen()

#Draws the menu screen with choice between Tron and Snake game modes
def choiceScreen():
	global titlePhotoImage, tronChoiceButton, snakeChoiceButton

	#Delete the title screen image
	screen.delete(titlePhotoImage)

	#Create and place buttons to allow the user to choose game mode
	tronChoiceButton = Button(screen, text='Play  Tron', font=('Courier', 18), command=tronGame)
	snakeChoiceButton = Button(screen, text='Play Snake', font=('Courier', 18), command=snakeGame)

	tronChoiceButton.place(x=2*840/3, y=672/2, anchor='center')
	snakeChoiceButton.place(x=840/3, y=672/2, anchor='center')

#Destroys the buttons forever
def buttonDestroy():
	global tronChoiceButton, snakeChoiceButton

	tronChoiceButton.destroy()
	snakeChoiceButton.destroy()

#Starts a game of tron
def tronGame():
	global master, screen
	
	#Destroy the buttons
	buttonDestroy()

	#Pass the tkinter objects to the tron game program
	tron.defineTkinter(master, screen)

	#Start a game of tron (passes control to the 'Tron Game.py' program)
	tron.playATronGame()

def snakeGame():
	global master, screen

	#Destroy the buttons
	buttonDestroy()

	#Pass the tkinter objects to the snake game program
	snake.defineTkinter(master, screen)

	#Start a game of snake (passes control to the 'Snake Multiplayer.py' program)
	snake.playASnakeGame()

#Runs the game
titleScreen()