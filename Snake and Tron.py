#==========================================#
#                                          #
# Multiplayer Snake & Tron Games           #
# By: Alex Foley                           #
# Code Written From May 29 - June 15, 2015 #
#                                          #
#==========================================#

#Imports
from tkinter import *
from configparser import *
tron = __import__('Tron Game')
snake = __import__('Snake Multiplayer')


#Runs the title screen
def titleScreen():
	global currentScreen, screen, titlePhotoImage, master, parser, configFilePath
	#set the value of the current screen
	currentScreen = 0

	#Allows read/write to Config file
	parser = RawConfigParser()
	configFilePath = './config.cfg'

	#Pull settings from config file
	parser.read(configFilePath)
	backgroundColour = parser.get('general', 'Background_Colour')

	#Create a tkinter instance and canvas
	master = Tk()
	screen = Canvas(master, width=840, height=672, background=backgroundColour)
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
def choiceScreen(fromOptions=False):
	global titlePhotoImage, tronChoiceButton, snakeChoiceButton, optionsChoiceButton
	global entryBox, backButton, writeButton, warningText

	#Delete the title screen image
	screen.delete(titlePhotoImage)

	#Create and place buttons to allow the user to choose game mode
	tronChoiceButton = Button(screen, text='Play  Tron', font=('Courier', 18), command=tronGame)
	snakeChoiceButton = Button(screen, text='Play Snake', font=('Courier', 18), command=snakeGame)
	optionsChoiceButton = Button(screen, text='Options', font=('Courier', 18), command=optionsScreen)

	tronChoiceButton.place(x=2*840/3, y=672/3, anchor='center')
	snakeChoiceButton.place(x=840/3, y=672/3, anchor='center')
	optionsChoiceButton.place(x=840/2, y=2*672/3, anchor='center')
	
	if fromOptions:
		entryBox.destroy()
		writeButton.destroy()
		backButton.destroy()
		screen.delete(warningText)

def optionsScreen():
	global writeButton, entryBox, warningText, outlineColour, backButton, warningText
	buttonDestroy()

	warningText = screen.create_text(840/2, 100, text='Warning: updating the config values could cause the game to crash\n\n' 
										+ 'To update background, type "Background_Colour = "and add your desired colour\n\n'
										+ 'To update a player colour, type "Player_playerNum_Colour = " and add your desired\n'
										+ '        colour, where playerNum is the number of the player you want to change.\n\n'
										+ 'To apply, press write (For background colour to update: close and re-run the game).', font=('Courier', 12))

	entryBox = Entry(screen, width=30, font=('Courier', 16))
	writeButton = Button(screen, text='Write', font=('Courier', 12), command=writeConfig)
	backButton = Button(screen, text='Back', font=('Courier', 16), command=backAScreen)

	entryBox.place(x=2*840/3, y=672/2, anchor='e')
	writeButton.place(x=2*840/3, y=672/2, anchor='w')
	backButton.place(x=840/2, y=2*672/3, anchor='center')

def backAScreen():
	choiceScreen(True)

def writeConfig():
	global entryBox, parser, configFilePath
	parameter, value = entryBox.get().strip(' ').split('=')
	parser.set('general', parameter, value)
	with open('./config.cfg', mode='w') as config:
		parser.write(config)


#Destroys the buttons forever
def buttonDestroy():
	global tronChoiceButton, snakeChoiceButton, optionsChoiceButton

	tronChoiceButton.destroy()
	snakeChoiceButton.destroy()
	optionsChoiceButton.destroy()

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