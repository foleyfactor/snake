from tkinter import *
from time import *
from random import *

#Initialize all of the game's variables
def setInitialVariables():
	global screenWidth, screenHeight, buttonChoice, arrayOfSnakes, gameRunning
	global playerColoursArray, apple, deadSnakes, deathOrder, winner, tie, scoreText
	global replayButton, gameOver
	
	screenWidth = 840
	screenHeight = 672

	gameRunning = True

	playerColoursArray = ['blue', 'red', 'green', 'yellow']
	arrayOfSnakes = []
	buttonChoice = 0
	apple = Apple()

	winner = None
	tie = None
	deathOrder = []
	
	scoreText = None
	deadSnakes = None

#Class for the snakes
class Snake(object):

	#Initialize the snake's variables and position
	def __init__(self, playerNum, totalPlayers):
		self.snakeArray = [None]*50
		self.snakeParts = [None]*50
		self.direction = choice(['Up', 'Down', 'Left', 'Right'])
		if totalPlayers > 1:
			self.playerNum = playerNum
		else:
			self.playerNum = ''
		self.colour = playerColoursArray[playerNum-1]
		self.speed = 14
		self.halfPieceSize = 7
		self.alive = True
		self.snakeLabel = None
		if totalPlayers == 1:
			self.snakeArray[0] = [screenWidth/2-7, screenHeight/2-7]
		elif totalPlayers == 2:
			self.snakeArray[0] = [playerNum*screenWidth/3-7, playerNum*screenHeight/3-7]
		elif totalPlayers == 4:
			horizontalCoefficient = 2 - playerNum % 2
			if playerNum > 2:
				verticalCoefficient = 2
			else:
				verticalCoefficient = 1
			self.snakeArray[0] = [horizontalCoefficient*screenWidth/3-7, verticalCoefficient*screenHeight/3-7]
		else:
			if playerNum == 1:
				self.snakeArray[0] = [screenWidth/2-7, screenHeight/3-7]
			else:
				self.snakeArray[0] = [(playerNum-1)*screenWidth/3-7, 2*screenHeight/3-7]

	#Move and update the snake's position based on its current direction
	def updatePosition(self):
		self.lastDirection = self.direction
		if self.direction == 'Up':
			snakeLen = self.snakeArray.index(None)
			for i in range(snakeLen):
				x = snakeLen-i-1
				if x:
					self.snakeArray[x] = self.snakeArray[x-1]
			self.snakeArray[0] = [self.snakeArray[0][0], self.snakeArray[0][1]-self.speed]
		
		elif self.direction == 'Down':
			snakeLen = self.snakeArray.index(None)
			for i in range(snakeLen):
				x = snakeLen-i-1
				if x:
					self.snakeArray[x] = self.snakeArray[x-1]
			self.snakeArray[0] = [self.snakeArray[0][0], self.snakeArray[0][1]+self.speed]
		
		elif self.direction == 'Left':
			snakeLen = self.snakeArray.index(None)
			for i in range(snakeLen):
				x = snakeLen-i-1
				if x:
					self.snakeArray[x] = self.snakeArray[x-1]
			
			self.snakeArray[0] = [self.snakeArray[0][0]-self.speed, self.snakeArray[0][1]]
		
		elif self.direction == 'Right':
			snakeLen = self.snakeArray.index(None)
			for i in range(snakeLen):
				x = snakeLen-i-1
				if x:
					self.snakeArray[x] = self.snakeArray[x-1]
			
			self.snakeArray[0] = [self.snakeArray[0][0]+self.speed, self.snakeArray[0][1]]

	#Procedure for drawing the snake
	def draw(self):
		for i in range(len(self.snakeArray)):
			if self.snakeArray[i] == None:
				break
			else:
				screen.delete(self.snakeParts[i])
		screen.delete(self.snakeLabel)

		for i in range(len(self.snakeArray)):
			if self.snakeArray[i] == None:
				break
			else:
				self.snakeParts[i] = screen.create_rectangle(self.snakeArray[i][0]-self.halfPieceSize, self.snakeArray[i][1]-self.halfPieceSize, self.snakeArray[i][0]+self.halfPieceSize, self.snakeArray[i][1]+self.halfPieceSize, fill=self.colour)
		
		self.snakeLabel = screen.create_text(self.snakeArray[0], text=str(self.playerNum), font=('Times New Roman', self.halfPieceSize*2), anchor='center')

	#Procedure to check if the snake is dead
	def checkDeath(self):

		#Check if the snake has run into the wall
		if self.snakeArray[0][0] - self.halfPieceSize < 0 or self.snakeArray[0][0] + self.halfPieceSize > screenWidth:
			self.alive = False
			deathOrder.append(self.playerNum)
		elif self.snakeArray[0][1] - self.halfPieceSize < 0 or self.snakeArray[0][1] + self.halfPieceSize > screenHeight:
			self.alive = False
			deathOrder.append(self.playerNum)

		#Check if the snake has run into itself
		if self.snakeArray[0] in self.snakeArray[2:]:
			self.alive = False
			deathOrder.append(self.playerNum)

		if not self.alive:
			self.kill()

	#Procedure to kill the snake and delete its parts
	def kill(self):
		self.alive = False
		for i in range(len(self.snakeArray)):
			if self.snakeArray[i] == None:
				break
			else:
				screen.delete(self.snakeParts[i])
		screen.delete(self.snakeLabel)

	#Function to check if a snake has collided with another snake
	def checkOtherSnakeCollision(self, otherSnake):
		if self.snakeArray[0] in otherSnake.snakeArray[1:]:
			self.alive = False
			deathOrder.append(self.playerNum)
		elif self.snakeArray[0] == otherSnake.snakeArray[0]:
			if self.snakeArray.index(None) > otherSnake.snakeArray.index(None):
				otherSnake.alive = False
				deathOrder.append(otherSnake.playerNum)
			elif otherSnake.snakeArray.index(None) > self.snakeArray.index(None):
				self.alive = False
				deathOrder.append(otherSnake.playerNum)
			elif otherSnake.snakeArray.index(None) == self.snakeArray.index(None):
				self.alive = False
				deathOrder.append(self.playerNum)
				otherSnake.alive = False
				deathOrder.append(otherSnake.playerNum)
		elif otherSnake.snakeArray[0] in self.snakeArray[1:]:
			otherSnake.alive = False
			deathOrder.append(otherSnake.playerNum)

		if not self.alive:
			self.kill()
		if not otherSnake.alive:
			otherSnake.kill()

	#Procedure to check if the snake has run into an apple
	def checkAppleCollision(self):
		if self.snakeArray[0] == apple.position:
			apple.beenHit()
			newSnakeIndex = self.snakeArray.index(None)
			self.snakeArray[newSnakeIndex] = self.snakeArray[newSnakeIndex-1]

#Class for the apple
class Apple(object):

	#Initialize the apple's variables and position
	def __init__(self):
		randomCoefficientX = randint(0,30)
		randomCoefficientY = randint(0,24)
		randomNegativeX = choice([1,-1])
		randomNegativeY = choice([1,-1])
		if randomCoefficientX == 30:
			randomNegativeX = 1
		if randomCoefficientY == 24:
			randomNegativeY = 1
		self.position = [screenWidth/2 + (14*randomCoefficientX*randomNegativeX)-7, screenHeight/2 + (14*randomCoefficientY*randomNegativeY)-7]
		self.apple = None

	#Procedure for drawing the apple
	def draw(self):
		screen.delete(self.apple)
		self.apple = screen.create_rectangle(self.position[0]-7, self.position[1]-7, self.position[0]+7, self.position[1]+7, fill='orange')		#screen.create_image(image=appleImage)
		screen.update()

	#Procedure called when the apple is hit
	def beenHit(self):
		randomCoefficientX = randint(0,30)
		randomCoefficientY = randint(0,24)
		randomNegativeX = choice([1,-1])
		randomNegativeY = choice([1,-1])
		if randomCoefficientX == 30:
			randomNegativeX = 1
		if randomCoefficientY == 24:
			randomNegativeY = 1
		self.position = [screenWidth/2 + (14*randomCoefficientX*randomNegativeX)-7, screenHeight/2 + (14*randomCoefficientY*randomNegativeY)-7]
		self.draw()

#Procedure for creating the menu screen for player selection
def menuScreen():
	global buttonChoice, onePlayerButton, twoPlayerButton, threePlayerButton, fourPlayerButton
	onePlayerButton = Button(screen, text='1  Player', font=('Courier', 18), command=buttonSet1)
	twoPlayerButton = Button(screen, text='2 Players', font=('Courier', 18), command=buttonSet2)
	threePlayerButton = Button(screen, text='3 Players', font=('Courier', 18), command=buttonSet3)
	fourPlayerButton = Button(screen, text='4 Players', font=('Courier', 18), command=buttonSet4)

	onePlayerButton.place(x=screenWidth/3, y=screenHeight/3, anchor='center')
	twoPlayerButton.place(x=2*screenWidth/3, y=screenHeight/3, anchor='center')
	threePlayerButton.place(x=screenWidth/3, y=2*screenHeight/3, anchor='center')
	fourPlayerButton.place(x=2*screenWidth/3, y=2*screenHeight/3, anchor='center')

#Button events
def buttonSet1():
	global buttonChoice
	buttonChoice = 1
	runGame()

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

#Procedure for updating all of the snake's positions
def updateSnakePositions():
	global deadSnakes, scoreText
	if scoreText:
		screen.delete(scoreText)
	if deadSnakes:
		screen.delete(deadSnakes)
	snakesDead = []
	for i in range(len(arrayOfSnakes)):
		if arrayOfSnakes[i].alive:
			arrayOfSnakes[i].checkAppleCollision()

			if not None in arrayOfSnakes[i].snakeArray:
				if len(arrayOfSnakes) > 1:
					otherSnakes = []
					for x in range(len(arrayOfSnakes)):
						if x == i:
							continue
						else:
							deathOrder.append(arrayOfSnakes[x]+arrayOfSnakes[x].playerNum)
							arrayOfSnakes[x].kill()
					arrayOfSnakes[i].kill()
				else:
					for w in range(50):
						arrayOfSnakes[i].snakeArray.append(None)
						arrayOfSnakes[i].snakeParts.append(None)

			arrayOfSnakes[i].checkDeath()
			arrayOfSnakes[i].updatePosition()
			arrayOfSnakes[i].draw()
		else:
			snakesDead.append(str(arrayOfSnakes[i].playerNum))
	if buttonChoice > 2:
		deadSnakes = screen.create_text(screenWidth/2, screenHeight/2, text='The following players are dead: ' + ', '.join(snakesDead))
	elif buttonChoice == 1 and goTimer < 0:
		scoreText = screen.create_text(screenWidth/2, 50, text=arrayOfSnakes[0].snakeArray.index(None), font=('Times New Roman', 20))
	screen.update()
	
#Procedure for checking for collisions between snakes
def checkSnakeCollisions():
	for i in range(len(arrayOfSnakes)):
		for x in range(len(arrayOfSnakes)):
			if i >= x or not arrayOfSnakes[i].alive:
				continue
			arrayOfSnakes[i].checkOtherSnakeCollision(arrayOfSnakes[x])

#Procedure for checking the state of a multiplayer snake game
def checkGameState():
	global deadSnakes, arrayOfSnakes, deathOrder, gameRunning, winner, tie
	if len(deathOrder) == len(arrayOfSnakes)-1:
		gameRunning = False
		winner = True
	elif len(deathOrder) == len(arrayOfSnakes):
		gameRunning = False
		tie = True

#Procedure for creating the game over message (multiplayer)
def gameOverMessage():
	global deadSnakes, arrayOfSnakes, deathOrder, replayButton, gameOver
	for i in range(len(arrayOfSnakes)):
		arrayOfSnakes[i].kill()
	screen.delete(deadSnakes)
	screen.delete(apple.apple)
	if winner:
		winningPlayer = [1,2,3,4]
		for i in deathOrder:
			winningPlayer.remove(i)
		gameOver = screen.create_text(screenWidth/2, screenHeight/2, font=("Courier", 18), text='This game\'s winner is: Player ' + str(winningPlayer[0]) + '!')
	elif tie:
		tiedPlayers = 'Player ' + str(min(deathOrder[-1], deathOrder[-2])) + ', and Player ' + str(max(deathOrder[-1], deathOrder[-2]))
		gameOver = screen.create_text(screenWidth/2, screenHeight/2, font=("Courier", 18), text='This game\'s winners are: ' + tiedPlayers + '!')

	replayButton = Button(screen, text='Play again', font=('Times New Roman', 16), command=replay)
	replayButton.place(x=screenWidth/2, y=3*screenHeight/4, anchor='center')



#Procedure for creating the game over message (single player)
def onePlayerGameOver():
	global gameOver, replayButton
	arrayOfSnakes[0].kill()
	screen.delete(scoreText)
	screen.delete(apple.apple)
	gameOver = screen.create_text(screenWidth/2, screenHeight/2, font=("Courier", 18) ,text='Game Over!\nYour score is: ' + str(arrayOfSnakes[0].snakeArray.index(None)))

	replayButton = Button(screen, text='Play again', font=('Times New Roman', 16), command=replay)
	replayButton.place(x=screenWidth/2, y=3*screenHeight/4, anchor='center')

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
	createSnakes()
	countDown()
	goTimer = 10
	apple.draw()
	if buttonChoice > 1:
		while gameRunning:
			updateSnakePositions()
			checkSnakeCollisions()
			checkGameState()
			if goTimer == 0:
				screen.delete(count)
			goTimer -= 1
			sleep(0.05)
		gameOverMessage()
	else:
		while arrayOfSnakes[0].alive:
			updateSnakePositions()
			if goTimer == 0:
				screen.delete(count)
			goTimer -= 1
			sleep(0.05)
		onePlayerGameOver()

#Quits the game
def quitGame():
	master.destroy()

#Creates snakes
def createSnakes():
	for i in range(1, buttonChoice+1):
		arrayOfSnakes.append(Snake(i, buttonChoice))
		arrayOfSnakes[i-1].draw()

#Destroys buttons
def killButtons():
	global onePlayerButton, twoPlayerButton, threePlayerButton, fourPlayerButton
	onePlayerButton.destroy()
	twoPlayerButton.destroy()
	threePlayerButton.destroy()
	fourPlayerButton.destroy()


#Handles key press events
def keyPressHandler(event):
	if event.keysym == 'Escape':
		quitGame()

	if buttonChoice:
		if event.keysym == 'Up':
			if arrayOfSnakes[0].lastDirection != 'Down':
				arrayOfSnakes[0].direction = 'Up'

		elif event.keysym == 'Down':
			if arrayOfSnakes[0].lastDirection != 'Up':
				arrayOfSnakes[0].direction = 'Down'

		elif event.keysym == 'Right':
			if arrayOfSnakes[0].lastDirection != 'Left':
				arrayOfSnakes[0].direction = 'Right'

		elif event.keysym == 'Left':
			if arrayOfSnakes[0].lastDirection != 'Right':
				arrayOfSnakes[0].direction = 'Left'
	
	if buttonChoice > 1:
		if event.keysym == 'w':
			if arrayOfSnakes[1].lastDirection != 'Down':
				arrayOfSnakes[1].direction = 'Up'

		elif event.keysym == 's':
			if arrayOfSnakes[1].lastDirection != 'Up':
				arrayOfSnakes[1].direction = 'Down'

		elif event.keysym == 'd':
			if arrayOfSnakes[1].lastDirection != 'Left':
				arrayOfSnakes[1].direction = 'Right'

		elif event.keysym == 'a':
			if arrayOfSnakes[1].lastDirection != 'Right':
				arrayOfSnakes[1].direction = 'Left'

	if buttonChoice > 2:
		if event.keysym == 't':
			if arrayOfSnakes[2].lastDirection != 'Down':
				arrayOfSnakes[2].direction = 'Up'

		elif event.keysym == 'g':
			if arrayOfSnakes[2].lastDirection != 'Up':
				arrayOfSnakes[2].direction = 'Down'

		elif event.keysym == 'h':
			if arrayOfSnakes[2].lastDirection != 'Left':
				arrayOfSnakes[2].direction = 'Right'

		elif event.keysym == 'f':
			if arrayOfSnakes[2].lastDirection != 'Right':
				arrayOfSnakes[2].direction = 'Left'

	if buttonChoice > 3:
		if event.keysym == 'i':
			if arrayOfSnakes[3].lastDirection != 'Down':
				arrayOfSnakes[3].direction = 'Up'

		elif event.keysym == 'k':
			if arrayOfSnakes[3].lastDirection != 'Up':
				arrayOfSnakes[3].direction = 'Down'

		elif event.keysym == 'l':
			if arrayOfSnakes[3].lastDirection != 'Left':
				arrayOfSnakes[3].direction = 'Right'

		elif event.keysym == 'j':
			if arrayOfSnakes[3].lastDirection != 'Right':
				arrayOfSnakes[3].direction = 'Left'

	if event.keysym == 'q':
		print(apple.position)

# def mouseClicker(event):
# 	print (event.x, event.y)

def replay():
	global gameOver, replayButton
	screen.delete(gameOver)
	replayButton.destroy()
	playASnakeGame()

def defineTkinter(passedMaster, passedScreen):
	global master, screen
	master = passedMaster
	screen = passedScreen

def playASnakeGame():
	global screen, master

	#Initializes the game's variables
	setInitialVariables()

	#Initializes the tkinter object and canvas
	#master = Tk()
	master.bind('<Key>', keyPressHandler)
	master.wm_title('Multiplayer Snake Battle')
	#master.bind('<1>', mouseClicker)
	#screen = Canvas(master, width=screenWidth, height=screenHeight)
	#screen.pack()

	#Starts the menu screen after 0.5 seconds and then runs the screen until infinity (or the window is closed)
	master.after(500, menuScreen())
	screen.focus_set()
	screen.mainloop()
