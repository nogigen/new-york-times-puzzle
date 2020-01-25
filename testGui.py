from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pygame
import os
import emoji
from clueGenerator import generate_clue
import random
from operator import itemgetter
import testdata


blackSquares = testdata.blackSquares
acrossClues = testdata.acrossClues
downClues = testdata.downClues
acrossWords = testdata.acrossWords
downWords = testdata.downWords
acrossSquares = testdata.acrossSquares
downSquares = testdata.downSquares
date = testdata.date

for i in range(len(acrossWords)):
	acrossWords[i] = acrossWords[i].upper()

for i in range(len(downWords)):
	downWords[i] = downWords[i].upper()
	
generated_across = []
generated_across_others = []
generated_down = []
generated_down_others = []

for across_word in acrossWords:
	
	generatedClue , possible_solutions = generate_clue(across_word)
	a = []
	# if generatedClue:
	# 	generated_across.append(generatedClue)	
	if generatedClue:
		a.extend([generatedClue])

	if possible_solutions:
		a.extend(possible_solutions)


	if len(a) == 0:
		generated_across_others.append(["couldn't generate a clue"])
	else:
		generated_across_others.append(a)
	


for down_word in downWords:
	
	generatedClue , possible_solutions = generate_clue(down_word)
	a = []
	if generatedClue:
		a.extend([generatedClue])
	# if generatedClue:
	# 	generated_down.append(generatedClue)

	if possible_solutions:
		a.extend(possible_solutions)

	if len(a) == 0:
		generated_down_others.append(["couldn't generate a clue"])
	else:
		generated_down_others.append(a)

print(generated_across_others)
print(len(generated_across_others))
print(len(generated_across_others[0]))
print(len(generated_across_others[1]))
print(len(generated_across_others[2]))
print(len(generated_across_others[3]))
print(len(generated_across_others[4]))

a1 = 0
a2 = 0
a3 = 0
a4 = 0
a5 = 0
d1 = 0
d2 = 0
d3 = 0
d4 = 0
d5 = 0
generated_across = [generated_across_others[0][0], generated_across_others[1][0], generated_across_others[2][0], generated_across_others[3][0], generated_across_others[4][0]]
generated_down = [generated_down_others[0][0], generated_down_others[1][0], generated_down_others[2][0], generated_down_others[3][0], generated_down_others[4][0]]

print(generated_across_others)
print(len(generated_across_others))

dark_blue = (0,0,139)
bright_red = (200,0,0)

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((1500,1000))

# title
pygame.display.set_caption("puzzle")

initialX = 150
initialY = 100
blockSize = 80

def showPuzzle(screen , initialX , initalY , blockSize , blackSquares , acrossWords , downWords , acrossSquares , downSquares , acrossClues , downClues , date, generated_across, generated_down):
	showDate(screen , date)
	showSquares(screen , initialX , initialY + 150, blockSize , blackSquares)
	showCharacters(screen , initialX , initialY + 150, blockSize , acrossSquares , downSquares, acrossWords)
	showLittleNumbers(screen , initialX , initialY + 150 , blockSize , acrossSquares , downSquares)	
	showAcrossClues(screen , acrossSquares , acrossClues)
	showDownClues(screen , downSquares , downClues)
	showGeneratedAcrossClues(screen, acrossSquares, generated_across)
	showGeneratedDownClues(screen, downSquares, generated_down)


def showDate(screen , date):
	x = 150
	y = 510 + 150
	smallText = pygame.font.Font("C:\\Windows\\Fonts\\seguiemj.ttf",20)
	groupName = "Artifically Intelligents"
	dateText = smallText.render(groupName + " - " + date, True, (0,0,0))
	screen.blit(dateText, (x,y))

def showSquares(screen , initialX , initialY, blockSize, blackSquares):
	black = (0,0,0)
	for i in range(25):
		row = i // 5
		column = i % 5

		# black square
		# str(i) since blackSquare list consists of "0" , "4" et cetera.
		if str(i) in blackSquares:
			pygame.draw.rect(screen , black , [initialX + column * blockSize , initialY + row * blockSize , blockSize , blockSize])

		else:
			pygame.draw.rect(screen , black , [initialX + column * blockSize , initialY + row * blockSize , blockSize , blockSize] , 1)

def showCharacters(screen , initialX , initalY , blockSize , acrossSquares , downSquares, acrossWords):
	count = 0
	j = 0
	aSquares = []
	for across in acrossSquares:
		# across[1] is a string since format is like ("1" , "1")
		aSquares.append(int(across[1]))

	while j < 25 and count != 5:
		entered = False
		if j in aSquares:
			word = acrossWords[count]
			count = count + 1
			row = j // 5 
			column = j % 5
			for i in range(len(word)):
				ch = word[i]
				# smallText = pygame.font.Font("freesansbold.ttf",64)
				# chText = smallText.render(ch, True, (0,0,0))
				# screen.blit(chText, (initialX + blockSize * column + i * blockSize + 15 , initialY + row * blockSize + 15))
				smallText = pygame.font.Font("C:\\Windows\\Fonts\\seguiemj.ttf",56)
				textSurf , textRect = smallText.render(ch , True , (0,0,0)) , smallText.render(ch, True, (0,0,0)).get_rect()
				textRect.center = ( (initialX + blockSize * column + blockSize / 2) , (initialY + 150 + blockSize * row + blockSize / 2 + 5) )
				screen.blit(textSurf , textRect)
				column = column + 1
				j = j + 1
				entered = True
		if not entered:
			j = j + 1

def showLittleNumbers(screen , initialX , initialY , blockSize , acrossSquares , downSquares):
	count = 0
	j = 0
	aletters = []
	aSquares = []
	for across in acrossSquares:
		# across[1] is a string since format is like ("1" , "1")
		aletters.append(across[0])
		aSquares.append(int(across[1]))

	# show the letters for accross words
	while j < 25:
		if j in aSquares:
			number = aletters[count]
			count = count + 1
			row = j // 5
			column = j % 5
			smallText = pygame.font.Font("C:\\Windows\\Fonts\\seguiemj.ttf",20)
			textSurf , textRect = smallText.render(str(number) , True , (0,0,0)) , smallText.render(str(number), True, (0,0,0)).get_rect()
			textRect.center = ( (initialX + blockSize * column + 10) , (initialY + blockSize * row  + 15) )
			screen.blit(textSurf , textRect)
		j = j + 1


	j = 0
	dletters = []
	dSquares = []
	count = 0
	for down in downSquares:
		# down[1] is a string since format is like ("1" , "1")
		dletters.append(down[0])
		dSquares.append(int(down[1]))

	# show the letters for down words
	while j < 25:
		if j in dSquares:
			if j in aSquares:
				count = count + 1
			else:
				number = dletters[count]
				count = count + 1
				row = j // 5
				column = j % 5
				smallText = pygame.font.Font("C:\\Windows\\Fonts\\seguiemj.ttf",20)
				textSurf , textRect = smallText.render(str(number) , True , (0,0,0)) , smallText.render(str(number), True, (0,0,0)).get_rect()
				textRect.center = ( (initialX + blockSize * column + 10) , (initialY + blockSize * row  + 15) )
				screen.blit(textSurf , textRect)
		j = j +1


def showGeneratedAcrossClues(screen, acrossSquares, generated_across):
	x = 700
	y = 120 + 370 -30
	# show "across"
	smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",20)
	textSurf , textRect = smallText.render("NEW ACROSS" , True , (0,0,0)) , smallText.render("NEW ACROSS", True, (0,0,0)).get_rect()
	textRect.center = ( (x + 30) , (y) )
	screen.blit(textSurf , textRect)

	# show across clues.
	for i in range(len(generated_across)):
		clue = generated_across[i]
		number = acrossSquares[i][0]

		# smallText = pygame.font.Font("freesansbold.ttf",10)
		# textSurf , textRect = smallText.render(str(number) + "   " + clue , True , (0,0,0)) , smallText.render(str(number) + "   " + clue, True, (0,0,0)).get_rect()
		# textRect.center = ( (x) , (y + (i+1) * 60) )
		# screen.blit(textSurf , textRect)
		if len(clue) > 45:
			lineNumber = (len(clue) // 45) + 1
			clues = []

			for c in range(lineNumber):
				if c != lineNumber - 1:
					clues.append(clue[c * 45 : (c + 1) * 45] + "-")
				else:
					clues.append(clue[c * 45 : len(clue)])

		
			curY = y + (i + 1) * 60
			for j in range(lineNumber):
				currentClue = clues[j]
				if j == 0:
					smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",12)
					clueText = smallText.render(str(number) + "  " + currentClue, True, (0,0,0))
					screen.blit(clueText, (x - 40, curY))

				else:
					smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",12)
					clueText = smallText.render(currentClue, True, (0,0,0))
					screen.blit(clueText, (x - 27, curY + 25))

					if j == lineNumber - 1:
						y = y + 35
					else:
						curY = curY + 25

		else:
			smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",12)
			# clueText = smallText.render(str(number) + "  " + emoji.demojize(clue), True, (0,0,0))
			clueText = smallText.render(str(number) + "  " + clue, True, (0,0,0))
			screen.blit(clueText, (x - 40 , y + (i+1) * 60))

def showAcrossClues(screen , acrossSquares , acrossClues):
	x = 700
	y = 120 - 60 - 30
	# show "across"
	smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",20)
	textSurf , textRect = smallText.render("ACROSS" , True , (0,0,0)) , smallText.render("ACROSS", True, (0,0,0)).get_rect()
	textRect.center = ( (x) , (y) )
	screen.blit(textSurf , textRect)

	# show across clues.
	for i in range(len(acrossClues)):
		clue = acrossClues[i]
		number = acrossSquares[i][0]

		# smallText = pygame.font.Font("freesansbold.ttf",10)
		# textSurf , textRect = smallText.render(str(number) + "   " + clue , True , (0,0,0)) , smallText.render(str(number) + "   " + clue, True, (0,0,0)).get_rect()
		# textRect.center = ( (x) , (y + (i+1) * 60) )
		# screen.blit(textSurf , textRect)
		if len(clue) > 45:
			lineNumber = (len(clue) // 45) + 1
			clues = []

			for c in range(lineNumber):
				if c != lineNumber - 1:
					clues.append(clue[c * 45 : (c + 1) * 45] + "-")
				else:
					clues.append(clue[c * 45 : len(clue)])
			curY = y + (i + 1) * 60
			for j in range(lineNumber):
				currentClue = clues[j]
				if j == 0:
					smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",12)
					clueText = smallText.render(str(number) + "  " + currentClue, True, (0,0,0))
					screen.blit(clueText, (x - 40, curY))

				else:
					smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",12)
					clueText = smallText.render(currentClue, True, (0,0,0))
					screen.blit(clueText, (x - 27, curY + 25))

					if j == lineNumber - 1:
						y = y + 35
					else:
						curY = curY + 25

		else:
			smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",12)
			# clueText = smallText.render(str(number) + "  " + emoji.demojize(clue), True, (0,0,0))
			clueText = smallText.render(str(number) + "  " + clue, True, (0,0,0))

			screen.blit(clueText, (x - 40 , y + (i+1) * 60))

def showGeneratedDownClues(screen, downSquares, downClues):
	x = 1100
	y = 120  + 370 -30

	# show "down"
	smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",20)
	textSurf , textRect = smallText.render("NEW DOWN" , True , (0,0,0)) , smallText.render("NEW DOWN", True, (0,0,0)).get_rect()
	textRect.center = ( (x + 20) , (y) )
	screen.blit(textSurf , textRect)

	# show down clues.
	for i in range(len(downClues)):
		clue = downClues[i]
		number = downSquares[i][0]

		# smallText = pygame.font.Font("freesansbold.ttf",10)
		# textSurf , textRect = smallText.render(str(number) + "   " + clue , True , (0,0,0)) , smallText.render(str(number) + "   " + clue, True, (0,0,0)).get_rect()
		# textRect.center = ( (x) , (y + (i+1) * 60) )
		# screen.blit(textSurf , textRect)
		if len(clue) > 45:
			lineNumber = (len(clue) // 45) + 1
			clues = []

			for c in range(lineNumber):
				if c != lineNumber - 1:
					clues.append(clue[c * 45 : (c + 1) * 45] + "-")
				else:
					clues.append(clue[c * 45 : len(clue)])

			curY = y + (i + 1) * 60
			for j in range(lineNumber):
				currentClue = clues[j]
				if j == 0:
					smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",12)
					clueText = smallText.render(str(number) + "  " + currentClue, True, (0,0,0))
					screen.blit(clueText, (x - 40 , curY))

				else:
					smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",12)
					clueText = smallText.render(currentClue, True, (0,0,0))
					screen.blit(clueText, (x - 27 , curY + 25))

					if j == lineNumber - 1:
						y = y + 35
					else:
						curY = curY + 25

		else:
			smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",12)
			clueText = smallText.render(str(number) + "  " + clue, True, (0,0,0))
			screen.blit(clueText, (x - 40 , y + (i+1) * 60))
def showDownClues(screen , downSquares , downClues):
	x = 1100
	y = 120 - 60 -30

	# show "down"
	smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",20)
	textSurf , textRect = smallText.render("DOWN" , True , (0,0,0)) , smallText.render("DOWN", True, (0,0,0)).get_rect()
	textRect.center = ( (x - 10) , (y) )
	screen.blit(textSurf , textRect)

	# show down clues.
	for i in range(len(downClues)):
		clue = downClues[i]
		number = downSquares[i][0]

		# smallText = pygame.font.Font("freesansbold.ttf",10)
		# textSurf , textRect = smallText.render(str(number) + "   " + clue , True , (0,0,0)) , smallText.render(str(number) + "   " + clue, True, (0,0,0)).get_rect()
		# textRect.center = ( (x) , (y + (i+1) * 60) )
		# screen.blit(textSurf , textRect)
		if len(clue) > 45:
			lineNumber = (len(clue) // 45) + 1
			clues = []

			for c in range(lineNumber):
				if c != lineNumber - 1:
					clues.append(clue[c * 45 : (c + 1) * 45] + "-")
				else:
					clues.append(clue[c * 45 : len(clue)])

			curY = y + (i + 1) * 60
			for j in range(lineNumber):
				currentClue = clues[j]
				if j == 0:
					smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",12)
					clueText = smallText.render(str(number) + "  " + currentClue, True, (0,0,0))
					screen.blit(clueText, (x - 40 , curY))

				else:
					smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",12)
					clueText = smallText.render(currentClue, True, (0,0,0))
					screen.blit(clueText, (x - 27 , curY + 25))

					if j == lineNumber - 1:
						y = y + 35
					else:
						curY = curY + 25

		else:
			smallText = pygame.font.Font("C:\\Windows\\Fonts\\arial.ttf",12)
			clueText = smallText.render(str(number) + "  " + clue, True, (0,0,0))
			screen.blit(clueText, (x - 40 , y + (i+1) * 60))


# gui
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill((255,255,255))

	pygame.draw.rect(screen, dark_blue, (520 + 150 -520, 880, 30,20))
	pygame.draw.rect(screen, dark_blue, (570 + 150 -520, 880, 30,20))
	pygame.draw.rect(screen, dark_blue, (620 + 150 -520, 880, 30,20))
	pygame.draw.rect(screen, dark_blue, (670 + 150 -520, 880, 30,20))
	pygame.draw.rect(screen, dark_blue, (720 + 150 -520, 880, 30,20))

	pygame.draw.rect(screen, bright_red, (920 + 150 -670, 880, 30,20))
	pygame.draw.rect(screen, bright_red, (970 + 150 -670, 880, 30,20))
	pygame.draw.rect(screen, bright_red, (1020 + 150 -670, 880, 30,20))
	pygame.draw.rect(screen, bright_red, (1070 + 150 -670, 880, 30,20))
	pygame.draw.rect(screen, bright_red, (1120 + 150 -670, 880, 30,20))

	click = pygame.mouse.get_pressed()
	if click[0] == 1:
		x_pos , y_pos = pygame.mouse.get_pos()
		x1_rect = 670 -520
		y_rect = 880
		w_rect = 30
		h_rect = 20
		x2_rect = 1070

		# change generate_across
		# across
		if x_pos > 670 -520 and x_pos < 700-520:
			if y_pos > 880 and y_pos < 900:
				# change across 1 clue
				if a1 != len(generated_across_others[0]) - 1:
					a1 = a1 + 1
				else:
					a1 = 0
				clues = generated_across_others[0]
				newClue = clues[a1]
				generated_across = [newClue, generated_across[1], generated_across[2], generated_across[3], generated_across[4]]
		if x_pos > 720-520 and x_pos < 750-520:
			if y_pos > 880 and y_pos < 900:
				# change across 2 clue
				if a2 != len(generated_across_others[1]) - 1:
					a2 = a2 + 1
				else:
					a2 = 0
				clues = generated_across_others[1]
				newClue = clues[a2]
				generated_across = [generated_across[0], newClue, generated_across[2], generated_across[3], generated_across[4]]
		if x_pos > 770-520 and x_pos < 800-520:
			if y_pos > 880 and y_pos < 900:
				# change across 3 clue
				if a3 != len(generated_across_others[2]) - 1:
					a3 = a3 + 1
				else:
					a3 = 0
				clues = generated_across_others[2]
				newClue = clues[a3]
				generated_across = [generated_across[0], generated_across[1], newClue, generated_across[3], generated_across[4]]
		if x_pos > 820-520 and x_pos < 850-520:
			if y_pos > 880 and y_pos < 900:
				# change across 4 clue
				if a4 != len(generated_across_others[3]) - 1:
					a4 = a4 + 1
				else:
					a4 = 0
				clues = generated_across_others[3]
				newClue = clues[a4]
				generated_across = [generated_across[0], generated_across[1], generated_across[2], newClue , generated_across[4]]
		if x_pos > 870-520 and x_pos < 900-520:
			if y_pos > 880 and y_pos < 900:
				# change across 5 clue
				if a5 != len(generated_across_others[4]) - 1:
					a5 = a5 + 1
				else:
					a5 = 0
				clues = generated_across_others[4]
				newClue = clues[a5]
				generated_across = [generated_across[0], generated_across[1], generated_across[2], generated_across[3], newClue]

		# generate generate_down
		# down
		if x_pos > 1070-670 and x_pos < 1100-670:
			if y_pos > 880 and y_pos < 900:
				# change down 1 clue
				if d1 != len(generated_down_others[0]) - 1:
					d1 = d1 + 1
				else:
					d1 = 0
				clues = generated_down_others[0]
				newClue = clues[d1]
				generated_down = [newClue, generated_down[1], generated_down[2], generated_down[3], generated_down[4]]
		if x_pos > 1120-670 and x_pos < 1150-670:
			if y_pos > 880 and y_pos < 900:
				# change down 2 clue
				if d2 != len(generated_down_others[1]) - 1:
					d2 = d2 + 1
				else:
					d2 = 0
				clues = generated_down_others[1]
				newClue = clues[d2]
				generated_down = [generated_down[0], newClue, generated_down[2], generated_down[3], generated_down[4]]
		if x_pos > 1170-670 and x_pos < 1200-670:
			if y_pos > 880 and y_pos < 900:
				# change down 3 clue
				if d3 != len(generated_down_others[2]) - 1:
					d3 = d3 + 1
				else:
					d3 = 0
				clues = generated_down_others[2]
				newClue = clues[d3]
				generated_down = [generated_down[0], generated_down[1], newClue, generated_down[3], generated_down[4]]
		if x_pos > 1220-670 and x_pos < 1250-670:
			if y_pos > 880 and y_pos < 900:
				# change down 4 clue
				if d4 != len(generated_down_others[3]) - 1:
					d4 = d4 + 1
				else:
					d4 = 0
				clues = generated_down_others[3]
				newClue = clues[d4]
				generated_down = [generated_down[0], generated_down[1], generated_down[2], newClue, generated_down[4]]
		if x_pos > 1270-670 and x_pos < 1300-670:
			if y_pos > 880 and y_pos < 900:
				# change down 5 clue
				if d5 != len(generated_down_others[4]) - 1:
					d5 = d5 + 1
				else:
					d5 = 0
				clues = generated_down_others[4]
				newClue = clues[d5]
				generated_down = [generated_down[0], generated_down[1], generated_down[2], generated_down[3], newClue]

	showPuzzle(screen , initialX , initialY, blockSize , blackSquares , acrossWords , downWords , acrossSquares , downSquares , acrossClues , downClues , date, generated_across, generated_down)
	
	pygame.display.update()