from tkinter import *
from time import *
from random import *
from configparser import *

#Initialize all of the game's variables
def setInitialVariables():
	global screenWidth, screenHeight, buttonChoice, arrayOfSnakes, gameRunning, appleImage
	global playerColoursArray, apple, deadSnakes, deathOrder, winner, tie, scoreText
	
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
	arrayOfSnakes = []
	buttonChoice = 0
	apple = Apple()

	winner = None
	tie = None
	deathOrder = []
	
	scoreText = None
	deadSnakes = None

	appleImage = PhotoImage(file='./appleNew.gif')

#Class for the snakes
class Snake(object):

	#Initialize the snake's variables and position based on the number of total players and player number
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

	#Draw the snake
	def draw(self):
		
		#Delete the snake's current pieces
		for i in range(len(self.snakeArray)):

			if self.snakeArray[i] == None:
				break
		
			else:
				screen.delete(self.snakeParts[i])
		
		#Delete the snake's label
		screen.delete(self.snakeLabel)

		#Draw all of the snake's parts
		for i in range(len(self.snakeArray)):

			if self.snakeArray[i] == None:
				break

			else:
				self.snakeParts[i] = screen.create_rectangle(self.snakeArray[i][0]-self.halfPieceSize, self.snakeArray[i][1]-self.halfPieceSize, self.snakeArray[i][0]+self.halfPieceSize, self.snakeArray[i][1]+self.halfPieceSize, fill=self.colour)
		
		#Redraw the snake's label
		self.snakeLabel = screen.create_text(self.snakeArray[0], text=str(self.playerNum), font=('Times New Roman', self.halfPieceSize*2), anchor='center')

	#Check if the snake is dead
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

	#Kill the snake and delete its parts
	def kill(self):
		
		#Set the snake's alive value to false
		self.alive = False

		#Delete all of the snake's pieces
		for i in range(len(self.snakeArray)):
			
			if self.snakeArray[i] == None:
				break
			
			else:
				screen.delete(self.snakeParts[i])
		
		#Delete the snake's label
		screen.delete(self.snakeLabel)

	#Check if a snake has collided with another snake
	def checkOtherSnakeCollision(self, otherSnake):
		
		#Check if this head collided with the other snake's body
		if self.snakeArray[0] in otherSnake.snakeArray[1:]:
			self.kill()
			deathOrder.append(self.playerNum)

		#Check if the snakes collide head to head
		elif self.snakeArray[0] == otherSnake.snakeArray[0]:

			#Kill the shorter snake (it gets eaten) or both (if they are the same length)
			if self.snakeArray.index(None) > otherSnake.snakeArray.index(None):
				otherSnake.kill()
				deathOrder.append(otherSnake.playerNum)

			elif otherSnake.snakeArray.index(None) > self.snakeArray.index(None):
				self.kill()
				deathOrder.append(otherSnake.playerNum)

			elif otherSnake.snakeArray.index(None) == self.snakeArray.index(None):
				self.kill()
				deathOrder.append(self.playerNum)
				otherSnake.kill()
				deathOrder.append(otherSnake.playerNum)

		#Check if the other snake's head collided with this snake's body
		elif otherSnake.snakeArray[0] in self.snakeArray[1:]:
			otherSnake.kill()
			deathOrder.append(otherSnake.playerNum)

	#Check if the snake has run into an apple
	def checkAppleCollision(self):
		
		#Check if the snake's head is at the apple
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

	#Draw the apple
	def draw(self):
		global appleImage

		screen.delete(self.apple)
		self.apple = screen.create_image(self.position, image=appleImage)

		screen.update()

	#When apple has been hit, generate new location
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

		#Ensures that the apple is not generated inside the body of one of the snakes
		for i in range(len(arrayOfSnakes)):
			if self.position in arrayOfSnakes[i].snakeArray:
				apple.beenHit()

		self.draw()

#Create the menu screen for player selection
def menuScreen():
	global buttonChoice, onePlayerButton, twoPlayerButton, threePlayerButton, fourPlayerButton

	#Initialize and place the buttons
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

#Update all of the snake's positions
def updateSnakePositions():
	global deadSnakes, scoreText

	#If necessary, delete the score text on the screen
	if scoreText:
		screen.delete(scoreText)

	#If necessary, delete the list of dead snakes
	if deadSnakes:
		screen.delete(deadSnakes)

	#Keeps track of which snakes are dead so it can be drawn on the screen
	snakesDead = []

	for i in range(len(arrayOfSnakes)):

		#If the snake is alive: update its position, check if it is dead, and draw it
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

		#If the snake is dead, add its number to the array of dead snakes
		else:
			snakesDead.append(str(arrayOfSnakes[i].playerNum))

	#Draw the list of dead snakes, if necessary (3-4 Players)
	if buttonChoice > 2:
		deadSnakes = screen.create_text(screenWidth/2, screenHeight/2, text='The following players are dead: ' + ', '.join(snakesDead))

	#Draw the player's score, if necessary (1 player)
	elif buttonChoice == 1 and goTimer < 0:
		scoreText = screen.create_text(screenWidth/2, 50, text=arrayOfSnakes[0].snakeArray.index(None), font=('Times New Roman', 20))

	#Update the screen
	screen.update()
	
#Check for collisions between snakes
def checkSnakeCollisions():

	for i in range(len(arrayOfSnakes)):
	
		for x in range(len(arrayOfSnakes)):
	
			if i >= x or not arrayOfSnakes[i].alive:
				continue
	
			arrayOfSnakes[i].checkOtherSnakeCollision(arrayOfSnakes[x])

#Checks the state of a multiplayer snake game
def checkGameState():
	global deadSnakes, arrayOfSnakes, deathOrder, gameRunning, winner, tie
	
	#If there is only one snake left, the game is over and there is a winner
	if len(deathOrder) == len(arrayOfSnakes)-1:
		gameRunning = False
		winner = True

	#If there are no snakes left, the game is over and there is a tie
	elif len(deathOrder) == len(arrayOfSnakes):
		gameRunning = False
		tie = True

#Create the game over message (multiplayer)
def gameOverMessage():
	global deadSnakes, arrayOfSnakes, deathOrder, replayButton, gameOver

	#Kill all of the snakes
	for i in range(len(arrayOfSnakes)):
		arrayOfSnakes[i].kill()

	#Delete the list of dead snakes, and the apple
	screen.delete(deadSnakes)
	screen.delete(apple.apple)

	#If there is a winner, determine the winning player's number and display it on the screen
	if winner:
		winningPlayer = [1,2,3,4]

		for i in deathOrder:
			winningPlayer.remove(i)

		gameOver = screen.create_text(screenWidth/2, screenHeight/2, font=("Courier", 18), text='This game\'s winner is: Player ' + str(winningPlayer[0]) + '!')

	#If there is a tie, determine the tied players' numbers and display them on the screen
	elif tie:
		tiedPlayers = 'Player ' + str(min(deathOrder[-1], deathOrder[-2])) + ', and Player ' + str(max(deathOrder[-1], deathOrder[-2]))
		gameOver = screen.create_text(screenWidth/2, screenHeight/2, font=("Courier", 18), text='This game\'s winners are: ' + tiedPlayers + '!')

	#Draw and place the play again button
	replayButton = Button(screen, text='Play again', font=('Times New Roman', 16), command=replay)
	replayButton.place(x=screenWidth/2, y=3*screenHeight/4, anchor='center')



#Create the the game over message (single player)
def onePlayerGameOver():
	global gameOver, replayButton

	#Kill the snake
	arrayOfSnakes[0].kill()

	#Delete the score and the apple
	screen.delete(scoreText)
	screen.delete(apple.apple)

	#Display the player's score on the screen
	gameOver = screen.create_text(screenWidth/2, screenHeight/2, font=("Courier", 18) ,text='Game Over!\nYour score is: ' + str(arrayOfSnakes[0].snakeArray.index(None)))

	#Create and place the play again button
	replayButton = Button(screen, text='Play again', font=('Times New Roman', 16), command=replay)
	replayButton.place(x=screenWidth/2, y=3*screenHeight/4, anchor='center')

#Counts down before the game begins
def countDown():
	global count

	#During the 3 second count down, update the text
	for i in range(3):
		count = screen.create_text(screenWidth/2, 50, text=str(3-i), font=('Times New Roman', 20), anchor='center')
		screen.update()
		sleep(1)
		screen.delete(count)

	#Delete the number and replace it with the text 'GO!'
	screen.delete(count)

	count = screen.create_text(screenWidth/2, 50, text='GO!', font=('Times New Roman', 20), anchor='center')

#Game's main procedure, responsible for running all of the game's methods
def runGame():
	global count, goTimer

	#Delete the buttons, create the snakes and start the count down
	killButtons()
	createSnakes()
	countDown()

	#Initializes the variable responsible for leaving the 'GO!' text on the screen
	goTimer = 10

	#Draw the apple
	apple.draw()

	#Multiplayer game
	if buttonChoice > 1:

		while gameRunning:

			#Update the snakes' positions, check for collisions between them, and check that that game is still not over
			updateSnakePositions()
			checkSnakeCollisions()
			checkGameState()

			#If necessary, delete the 'GO!' text
			if goTimer == 0:
				screen.delete(count)

			goTimer -= 1
			
			sleep(0.05)

		#Display the game over message	
		gameOverMessage()

	#Single player game
	else:

		while arrayOfSnakes[0].alive:

			#Update the snake's position
			updateSnakePositions()

			#If necessary, delete the 'GO!' text
			if goTimer == 0:
				screen.delete(count)

			goTimer -= 1
			
			sleep(0.05)

		#Display the game over message
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

#Replays the game with the current settings
def replay():
	global gameOver, replayButton, buttonChoice
	screen.delete(gameOver)
	replayButton.destroy()
	playASnakeGame(buttonChoice)

#Takes the tkinter objects from the 'Tron and Snake.py' program
def defineTkinter(passedMaster, passedScreen):
	global master, screen
	master = passedMaster
	screen = passedScreen

#Plays a game of snake
def playASnakeGame(numPlayers=None):
	global screen, master

	#Initializes the game's variables
	setInitialVariables()

	#Binds the keys and sets the room title
	master.bind('<Key>', keyPressHandler)
	master.wm_title('Multiplayer Snake Battle')

	#Allows replays to be run with the same settings, or displays the menu screen
	if not numPlayers:
		menuScreen()
	
	else:
		if numPlayers == 1:
			buttonSet1()
	
		elif numPlayers == 2:
			buttonSet2()
	
		elif numPlayers == 3:
			buttonSet3()
	
		else:
			buttonSet4()

	#Sets focus to the window and then runs the screen until infinity (or the window is closed)
	screen.focus_set()
	screen.mainloop()