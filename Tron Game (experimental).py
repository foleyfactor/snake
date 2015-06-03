from tkinter import *
from time import *
from random import *

#Initialize all of the game's variables
def setInitialVariables():
	global screenWidth, screenHeight, buttonChoice, arrayOfBikes, gameRunning, playerColoursArray, deadBikes, deathOrder, winner, tie, scoreText
	
	screenWidth = 840
	screenHeight = 672

	gameRunning = True

	playerColoursArray = ['blue', 'red', 'green', 'yellow']
	arrayOfBikes = []
	buttonChoice = 0

	winner = None
	tie = None
	deathOrder = []
	
	scoreText = None
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

	#Procedure for drawing the bike
	def draw(self):
		for i in range(len(self.bikeArray)):
			if self.bikeArray[i]:
				screen.delete(self.bikeParts[i])

		screen.delete(self.bikeLabel)

		for i in range(len(self.bikeArray)):
			if self.bikeArray[i]:
				self.bikeParts[i] = screen.create_rectangle(self.bikeArray[i][0]-self.halfPieceSize, self.bikeArray[i][1]-self.halfPieceSize, self.bikeArray[i][0]+self.halfPieceSize, self.bikeArray[i][1]+self.halfPieceSize, fill=self.colour)
		
		self.bikeLabel = screen.create_text(self.bikeArray[0], text=str(self.playerNum), font=('Times New Roman', self.halfPieceSize*2), anchor='center')

	#Procedure to check if the bike is dead
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

		if not self.alive:
			self.kill()

	#Procedure to kill the bike and delete its parts
	def kill(self):
		self.alive = False
		for i in range(len(self.bikeArray)):
			if self.bikeArray[i] == None:
				break
			else:
				screen.delete(self.bikeParts[i])
		screen.delete(self.bikeLabel)

	#Function to check if a bike has collided with another bike
	def checkOtherBikeCollision(self, otherBike):
		if self.bikeArray[0] in otherBike.bikeArray[1:]:
			self.alive = False
			deathOrder.append(self.playerNum)
		elif self.bikeArray[0] == otherBike.bikeArray[0]:
			if self.bikeArray.index(None) > otherBike.bikeArray.index(None):
				otherBike.alive = False
				deathOrder.append(otherBike.playerNum)
			elif otherBike.bikeArray.index(None) > self.bikeArray.index(None):
				self.alive = False
				deathOrder.append(otherBike.playerNum)
			elif otherBike.bikeArray.index(None) == self.bikeArray.index(None):
				self.alive = False
				deathOrder.append(self.playerNum)
				otherBike.alive = False
				deathOrder.append(otherBike.playerNum)
		elif otherBike.bikeArray[0] in self.bikeArray[1:]:
			otherBike.alive = False
			deathOrder.append(otherBike.playerNum)

		if not self.alive:
			self.kill()
		if not otherBike.alive:
			otherBike.kill()

#Procedure for creating the menu screen for player selection
def menuScreen():
	global buttonChoice, twoPlayerButton, threePlayerButton, fourPlayerButton
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

#Procedure for updating all of the bike's positions
def updateBikePositions():
	global deadBikes, scoreText
	if scoreText:
		screen.delete(scoreText)
	if deadBikes:
		screen.delete(deadBikes)
	bikesDead = []
	for i in range(len(arrayOfBikes)):
		if arrayOfBikes[i].alive:
			arrayOfBikes[i].checkDeath()
			arrayOfBikes[i].updatePosition()
			arrayOfBikes[i].draw()
		else:
			bikesDead.append(str(arrayOfBikes[i].playerNum))
	if buttonChoice > 2:
		deadBikes = screen.create_text(screenWidth/2, screenHeight/2, text='The following players are dead: ' + ', '.join(bikesDead))
	screen.update()
	
#Procedure for checking for collisions between bikes
def checkBikeCollisions():
	for i in range(len(arrayOfBikes)):
		for x in range(len(arrayOfBikes)):
			if i >= x or not arrayOfBikes[i].alive:
				continue
			arrayOfBikes[i].checkOtherBikeCollision(arrayOfBikes[x])

#Procedure for checking the state of a multiplayer bike game
def checkGameState():
	global deadBikes, arrayOfBikes, deathOrder, gameRunning, winner, tie
	if len(deathOrder) == len(arrayOfBikes)-1:
		gameRunning = False
		winner = True
	elif len(deathOrder) == len(arrayOfBikes):
		gameRunning = False
		tie = True

#Procedure for creating the game over message (multiplayer)
def gameOverMessage():
	global deadBikes, arrayOfBikes, deathOrder
	for i in range(len(arrayOfBikes)):
		arrayOfBikes[i].kill()
	screen.delete(deadBikes)
	if winner:
		winningPlayer = [1,2,3,4]
		for i in deathOrder:
			winningPlayer.remove(i)
		screen.create_text(screenWidth/2, screenHeight/2, font=("Courier", 18), text='This game\'s winner is: Player ' + str(winningPlayer[0]) + '!')
	elif tie:
		tiedPlayers = 'Player ' + str(min(deathOrder[-1], deathOrder[-2])) + ', and Player ' + str(max(deathOrder[-1], deathOrder[-2]))
		screen.create_text(screenWidth/2, screenHeight/2, font=("Courier", 18), text='This game\'s winners are: ' + tiedPlayers + '!')

#Procedure for creating the game over message (single player)
def onePlayerGameOver():
	arrayOfBikes[0].kill()
	screen.delete(scoreText)
	screen.create_text(screenWidth/2, screenHeight/2, font=("Courier", 18) ,text='Game Over!\nYour score is: ' + str(arrayOfBikes[0].bikeArray.index(None)))

#Procedure for the count down before the game begins
def countDown():
	global count
	count = None
	for i in range(3):
		count = screen.create_text(screenWidth/2, 50, text=str(3-i), font=('Times New Roman', 20), anchor='center')
		screen.update()
		sleep(1)
		screen.delete(count)
	screen.delete(count)
	count = screen.create_text(screenWidth/2, 50, text='GO!', font=('Times New Roman', 20), anchor='center')

#Game's main procedure, responsible for running all of the game's methods
def runGame():
	global count, goTimer
	killButtons()
	createBikes()
	countDown()
	goTimer = 10
	if buttonChoice > 1:
		while gameRunning:
			updateBikePositions()
			checkBikeCollisions()
			checkGameState()
			if goTimer == 0:
				screen.delete(count)
			goTimer -= 1
			sleep(0.05)
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

# def mouseClicker(event):
# 	print (event.x, event.y)


#Initializes the game's variables
setInitialVariables()

#Initializes the tkinter object and canvas
master = Tk()
master.bind('<Key>', keyPressHandler)
master.wm_title('Multiplayer Bike Battle')
#master.bind('<1>', mouseClicker)
screen = Canvas(master, width=screenWidth, height=screenHeight)
screen.pack()

screen.focus_set()

#Starts the menu screen after 0.5 seconds and then runs the screen until infinity (or the window is closed)
master.after(500, menuScreen())
screen.mainloop()