from tkinter import *
from time import *
from random import *
from configparser import *

#Initialize all of the game's variables
def setInitialVariables():
	global screenWidth, screenHeight, buttonChoice, arrayOfBikes, gameRunning
	global playerColoursArray, deadBikes, deathOrder, winner, tie
	
	#Allows values to be taken from the config file
	parser = ConfigParser()
	configFilePath = './config.cfg'

	#Pull settings from config file
	parser.read(configFilePath)
	player1Colour = parser.get('general', 'Player_1_Colour')
	player2Colour = parser.get('general', 'Player_2_Colour')
	player3Colour = parser.get('general', 'Player_3_Colour')
	player4Colour = parser.get('general', 'Player_4_Colour')

	screenWidth = 840
	screenHeight = 672

	gameRunning = True

	playerColoursArray = [player1Colour, player2Colour, player3Colour, player4Colour]
	arrayOfBikes = []
	buttonChoice = 0

	winner = None
	tie = None
	deathOrder = []
	
	deadBikes = None

#Class for the bikes
class Bike(object):

	#Initialize the bike's variables and position
	def __init__(self, playerNum, totalPlayers):
		self.bikeArray = [None]
		self.bikeParts = [None]

		self.direction = choice(['Up', 'Down', 'Left', 'Right'])

		self.playerNum = playerNum

		self.colour = playerColoursArray[playerNum-1]
		self.speed = 14
		self.halfPieceSize = 7

		self.alive = True
		self.bikeLabel = None

		if totalPlayers == 2:
			self.bikeArray[0] = [playerNum*screenWidth/3-7, playerNum*screenHeight/3-7]

		elif totalPlayers == 4:
			horizontalCoefficient = 2 - playerNum % 2

			if playerNum > 2:
				verticalCoefficient = 2

			else:
				verticalCoefficient = 1

			self.bikeArray[0] = [horizontalCoefficient*screenWidth/3-7, verticalCoefficient*screenHeight/3-7]

		else:
			if playerNum == 1:
				self.bikeArray[0] = [screenWidth/2-7, screenHeight/3-7]

			else:
				self.bikeArray[0] = [(playerNum-1)*screenWidth/3-7, 2*screenHeight/3-7]

	#Move and update the bike's position based on its current direction
	def updatePosition(self):
		self.bikeArray.append(None)
		self.bikeParts.append(None)

		self.lastDirection = self.direction

		#Only update the bike if it is still alive
		if self.alive:

			#Based on the bike's direction, add a new piece to it
			if self.direction == 'Up':

				for i in range(len(self.bikeArray)):
					x = len(self.bikeArray)-i-1

					if x:
						self.bikeArray[x] = self.bikeArray[x-1]

				self.bikeArray[0] = [self.bikeArray[0][0], self.bikeArray[0][1]-self.speed]
			
			elif self.direction == 'Down':

				for i in range(len(self.bikeArray)):
					x = len(self.bikeArray)-i-1

					if x:
						self.bikeArray[x] = self.bikeArray[x-1]

				self.bikeArray[0] = [self.bikeArray[0][0], self.bikeArray[0][1]+self.speed]
			
			elif self.direction == 'Left':

				for i in range(len(self.bikeArray)):
					x = len(self.bikeArray)-i-1

					if x:
						self.bikeArray[x] = self.bikeArray[x-1]
				
				self.bikeArray[0] = [self.bikeArray[0][0]-self.speed, self.bikeArray[0][1]]
			
			elif self.direction == 'Right':

				for i in range(len(self.bikeArray)):
					x = len(self.bikeArray)-i-1

					if x:
						self.bikeArray[x] = self.bikeArray[x-1]
				
				self.bikeArray[0] = [self.bikeArray[0][0]+self.speed, self.bikeArray[0][1]]

	#Draws the bike
	def draw(self):

		#Delete all of the bike's pieces
		for i in range(len(self.bikeArray)):

			if self.bikeArray[i]:
				screen.delete(self.bikeParts[i])

		#Delete the player number label on the bike
		screen.delete(self.bikeLabel)

		#If the bike is alive, draw the its pieces
		if self.alive:

			for i in range(len(self.bikeArray)):

				if self.bikeArray[i]:
					self.bikeParts[i] = screen.create_rectangle(self.bikeArray[i][0]-self.halfPieceSize, self.bikeArray[i][1]-self.halfPieceSize, self.bikeArray[i][0]+self.halfPieceSize, self.bikeArray[i][1]+self.halfPieceSize, fill=self.colour)
			
			self.bikeLabel = screen.create_text(self.bikeArray[0], text=str(self.playerNum), font=('Times New Roman', self.halfPieceSize*2), anchor='center')

	#Checks if the bike is dead
	def checkDeath(self):

		#Check if the bike has run into the wall
		if self.bikeArray[0][0] - self.halfPieceSize < 0 or self.bikeArray[0][0] + self.halfPieceSize > screenWidth:
			self.alive = False
			deathOrder.append(self.playerNum)

		elif self.bikeArray[0][1] - self.halfPieceSize < 0 or self.bikeArray[0][1] + self.halfPieceSize > screenHeight:
			self.alive = False
			deathOrder.append(self.playerNum)

		#Check if the bike has run into itself
		if self.bikeArray[0] in self.bikeArray[2:]:
			self.alive = False
			deathOrder.append(self.playerNum)

		#If the snake is not alive, call its kill procedure
		if not self.alive:
			self.kill()

	#Kills the bike and delete its parts
	def kill(self):

		#Update the bike's alive state to False
		self.alive = False

		#Delete all of the bike's parts
		for i in range(len(self.bikeArray)):

			if self.bikeArray[i] == None:
				break

			else:
				screen.delete(self.bikeParts[i])

		#Delete the player label on the bike and set its array
		screen.delete(self.bikeLabel)
		self.bikeArray = [None, None]

	#Checks if a bike has collided with another bike
	def checkOtherBikeCollision(self, otherBike):

		if self.bikeArray[0] in otherBike.bikeArray[1:]:
			deathOrder.append(self.playerNum)
			self.kill()

		elif self.bikeArray[0] == otherBike.bikeArray[0]:
			deathOrder.append(self.playerNum)
			deathOrder.append(otherBike.playerNum)
			self.kill()
			otherBike.kill()

		elif otherBike.bikeArray[0] in self.bikeArray[1:]:
			deathOrder.append(otherBike.playerNum)
			otherBike.kill()

#Creates the menu screen for player selection
def menuScreen():
	global buttonChoice, twoPlayerButton, threePlayerButton, fourPlayerButton

	#Initialize and place the buttons
	twoPlayerButton = Button(screen, text='2 Players', font=('Courier', 18), command=buttonSet2)
	threePlayerButton = Button(screen, text='3 Players', font=('Courier', 18), command=buttonSet3)
	fourPlayerButton = Button(screen, text='4 Players', font=('Courier', 18), command=buttonSet4)

	twoPlayerButton.place(x=screenWidth/2, y=screenHeight/3, anchor='center')
	threePlayerButton.place(x=screenWidth/3, y=2*screenHeight/3, anchor='center')
	fourPlayerButton.place(x=2*screenWidth/3, y=2*screenHeight/3, anchor='center')

#Button events
def buttonSet2():
	global buttonChoice
	buttonChoice = 2
	runGame()

def buttonSet3():
	global buttonChoice
	buttonChoice = 3
	runGame()

def buttonSet4():
	global buttonChoice
	buttonChoice = 4
	runGame()

#Updates all of the bikes' positions.
def updateBikePositions():
	global deadBikes

	#If there is a need to display the dead bikes (3 or 4 players) delete the text on the screen
	if deadBikes:
		screen.delete(deadBikes)

	#Keeps track of which bikes are dead
	bikesDead = []

	#Go through all of the bikes and, if they are alive, update their positions, draw them, and check that they haven't died yet
	for i in range(len(arrayOfBikes)):

		if arrayOfBikes[i].alive:
			arrayOfBikes[i].checkDeath()
			arrayOfBikes[i].updatePosition()
			arrayOfBikes[i].draw()

		else:
			bikesDead.append(str(arrayOfBikes[i].playerNum))

	#If there is a need to display the dead bikes (3 or 4 players), rederaw the text on the screen.
	if buttonChoice > 2:
		deadBikes = screen.create_text(screenWidth/2, screenHeight/2, text='The following players are dead: ' + ', '.join(bikesDead))

	screen.update()
	
#Checks for collisions between bikes
def checkBikeCollisions():
	
	#Loops through and calls the procedure to check for the collision between bikes
	for i in range(len(arrayOfBikes)):
	
		for x in range(len(arrayOfBikes)):
	
			if i >= x or not arrayOfBikes[i].alive:
				continue
	
			arrayOfBikes[i].checkOtherBikeCollision(arrayOfBikes[x])

#Checks the state of a game
def checkGameState():
	global deadBikes, arrayOfBikes, deathOrder, gameRunning, winner, tie

	#If there is only one bike left, the game is over and there is a winner
	if len(deathOrder) == len(arrayOfBikes)-1:
		gameRunning = False
		winner = True

	#If there are no bikes left, the game is over and there is a tie
	elif len(deathOrder) == len(arrayOfBikes):
		gameRunning = False
		tie = True

#Creates the game over message
def gameOverMessage():
	global deadBikes, arrayOfBikes, deathOrder, replayButton, gameOver

	#Kill the remaining bikes
	for i in range(len(arrayOfBikes)):
		arrayOfBikes[i].kill()

	#Delete the list of dead bikes
	screen.delete(deadBikes)

	#If there is a winner, find out which bike won, and declare that bike the winner
	if winner:
		winningPlayer = [1,2,3,4]
		for i in deathOrder:
			winningPlayer.remove(i)
		gameOver = screen.create_text(screenWidth/2, screenHeight/2, font=("Courier", 18), text='This game\'s winner is: Player ' + str(winningPlayer[0]) + '!')

	#If there is a tie, determine the tied players and declare them winners
	elif tie:
		tiedPlayers = 'Player ' + str(min(deathOrder[-1], deathOrder[-2])) + ', and Player ' + str(max(deathOrder[-1], deathOrder[-2]))
		gameOver = screen.create_text(screenWidth/2, screenHeight/2, font=("Courier", 18), text='This game\'s winners are: ' + tiedPlayers + '!')

	#Create and place a 'play again' button
	replayButton = Button(screen, text='Play again', font=('Times New Roman', 16), command=replay)
	replayButton.place(x=screenWidth/2, y=3*screenHeight/4, anchor='center')

#Counts down before the game begins
def countDown():
	global count

	#Count down from 3 to 1
	for i in range(3):
		count = screen.create_text(screenWidth/2, 50, text=str(3-i), font=('Times New Roman', 20), anchor='center')
		screen.update()
		sleep(1)
		screen.delete(count)

	#Delete the count number
	screen.delete(count)

	#Create the text 'GO!'
	count = screen.create_text(screenWidth/2, 50, text='GO!', font=('Times New Roman', 20), anchor='center', tags='go')

#Game's main procedure, responsible for running all of the game's methods
def runGame():
	global count, goTimer

	#Delete the buttons
	killButtons()

	#Create the bikes
	createBikes()

	#Start the count down timer
	countDown()

	#Controls how long the 'GO!' stays on
	goTimer = 10

	#Game's main loop
	while gameRunning:
		#Update the bikes' positions, check for collisions and check the state of the game
		updateBikePositions()
		checkBikeCollisions()
		checkGameState()

		#If the timer is at 0, delete the 'GO!' text
		if goTimer == 0:
			screen.delete('go')

		#Lower the timer count by 1
		goTimer -= 1

		sleep(0.05)

	#Display the game over message
	gameOverMessage()

#Quits the game
def quitGame():
	master.destroy()

#Creates bikes
def createBikes():
	for i in range(1, buttonChoice+1):
		arrayOfBikes.append(Bike(i, buttonChoice))
		arrayOfBikes[i-1].draw()

#Destroys buttons
def killButtons():
	global twoPlayerButton, threePlayerButton, fourPlayerButton
	twoPlayerButton.destroy()
	threePlayerButton.destroy()
	fourPlayerButton.destroy()


#Handles key press events
def keyPressHandler(event):
	if event.keysym == 'Escape':
		quitGame()

	if buttonChoice:
		if event.keysym == 'Up':
			if arrayOfBikes[0].lastDirection != 'Down':
				arrayOfBikes[0].direction = 'Up'

		elif event.keysym == 'Down':
			if arrayOfBikes[0].lastDirection != 'Up':
				arrayOfBikes[0].direction = 'Down'

		elif event.keysym == 'Right':
			if arrayOfBikes[0].lastDirection != 'Left':
				arrayOfBikes[0].direction = 'Right'

		elif event.keysym == 'Left':
			if arrayOfBikes[0].lastDirection != 'Right':
				arrayOfBikes[0].direction = 'Left'
	
		if event.keysym == 'w':
			if arrayOfBikes[1].lastDirection != 'Down':
				arrayOfBikes[1].direction = 'Up'

		elif event.keysym == 's':
			if arrayOfBikes[1].lastDirection != 'Up':
				arrayOfBikes[1].direction = 'Down'

		elif event.keysym == 'd':
			if arrayOfBikes[1].lastDirection != 'Left':
				arrayOfBikes[1].direction = 'Right'

		elif event.keysym == 'a':
			if arrayOfBikes[1].lastDirection != 'Right':
				arrayOfBikes[1].direction = 'Left'

	if buttonChoice > 2:
		if event.keysym == 't':
			if arrayOfBikes[2].lastDirection != 'Down':
				arrayOfBikes[2].direction = 'Up'

		elif event.keysym == 'g':
			if arrayOfBikes[2].lastDirection != 'Up':
				arrayOfBikes[2].direction = 'Down'

		elif event.keysym == 'h':
			if arrayOfBikes[2].lastDirection != 'Left':
				arrayOfBikes[2].direction = 'Right'

		elif event.keysym == 'f':
			if arrayOfBikes[2].lastDirection != 'Right':
				arrayOfBikes[2].direction = 'Left'

	if buttonChoice > 3:
		if event.keysym == 'i':
			if arrayOfBikes[3].lastDirection != 'Down':
				arrayOfBikes[3].direction = 'Up'

		elif event.keysym == 'k':
			if arrayOfBikes[3].lastDirection != 'Up':
				arrayOfBikes[3].direction = 'Down'

		elif event.keysym == 'l':
			if arrayOfBikes[3].lastDirection != 'Left':
				arrayOfBikes[3].direction = 'Right'

		elif event.keysym == 'j':
			if arrayOfBikes[3].lastDirection != 'Right':
				arrayOfBikes[3].direction = 'Left'

#Takes the tkinter objects from the 'Snake and Tron' program
def defineTkinter(passedMaster, passedScreen):
	global master, screen
	master = passedMaster
	screen = passedScreen

#Plays the game again with the same settings
def replay():
	global replayButton, gameOver, buttonChoice
	screen.delete(gameOver)
	replayButton.destroy()
	playATronGame(buttonChoice)

#Plays a game of Tron
def playATronGame(numPlayers=None):
	global screen, master
	
	#Initializes the game's variables
	setInitialVariables()

	#Binds keys and sets room title
	master.bind('<Key>', keyPressHandler)
	master.wm_title('Multiplayer Tron Battle')

	#Handles menu screen/replay functions
	if not numPlayers:
		menuScreen()
	else:
		if numPlayers == 2:
			buttonSet2()
		elif numPlayers == 3:
			buttonSet3()
		else:
			buttonSet4()

	#Sets focus on the window and runs the screen until infinity (or the window is closed)
	screen.focus_set()
	screen.mainloop()