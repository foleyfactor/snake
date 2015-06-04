from tkinter import *
tron = __import__('Tron Game')
snake = __import__('Snake Multiplayer')

def titleScreen():
	global currentScreen, screen, titlePhotoImage, master
	currentScreen = 0
	master = Tk()
	screen = Canvas(master, width=840, height=672)
	screen.pack()
	screen.focus_set()
	master.bind('<Key>', nextScreen)
	master.wm_title('Snake and Tron')

	titlePhoto = PhotoImage(file='./titleScreenPhoto.gif')
	titlePhotoImage = screen.create_image(420, 336, image=titlePhoto, anchor='center')
	screen.mainloop()

def nextScreen(event):
	global currentScreen
	if currentScreen == 0:
		currentScreen = 1
		choiceScreen()

def choiceScreen():
	global titlePhotoImage
	screen.delete(titlePhotoImage)
	tronChoiceButton = Button(screen, text='Play  Tron', font=('Courier', 18), command=tronGame)
	snakeChoiceButton = Button(screen, text='Play Snake', font=('Courier', 18), command=snakeGame)

	tronChoiceButton.place(x=2*840/3, y=672/2, anchor='center')
	snakeChoiceButton.place(x=840/3, y=672/2, anchor='center')

def tronGame():
	global master
	master.destroy()
	tron.playATronGame()

def snakeGame():
	global master
	master.destroy()
	snake.playASnakeGame()

titleScreen()