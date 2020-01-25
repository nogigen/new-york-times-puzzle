from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pygame
import os
import emoji
from clueGenerator import generate_clue
import random
from operator import itemgetter


okBtn = None
while okBtn == None:
	try:
		driver = webdriver.Chrome(os.getcwd() + "\\chromedriver.exe")
		url = "https://www.nytimes.com/crosswords/game/mini"
		driver.get(url)
		time.sleep(3)

		okBtn = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button/div/span')
		okBtn.click()

		revealBtn = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button')
		revealBtn.click()

		revealPuzzleBtn = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a')
		revealPuzzleBtn.click()

		confirmBtn = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/article/div[2]/button[2]/div/span')
		confirmBtn.click()

		crossBtn = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/span')
		crossBtn.click()

		soup = BeautifulSoup(driver.page_source, 'lxml')
	except:
		print("try again :(")
		# reset
		okBtn = None
		driver.close()
		
# get date
dateText = soup.find('div' , {'class' : 'PuzzleDetails-date--1HNzj'})
date = dateText.get_text()

# fill acrossClues list
# fill downClues list
ol = soup.find_all('ol', {'class' : 'ClueList-list--2dD5-'})
up = ol[0]
down = ol[1]
acrossClues = []
downClues = []
acrossNumbers = []
downNumbers = []
for li in up:
	span = li.find_all('span')
	acrossNumbers.append(span[0].get_text())
	acrossClues.append(span[1].get_text())


for li in down:
	span = li.find_all('span')
	downNumbers.append(span[0].get_text())
	downClues.append(span[1].get_text())

###
# adding number of black squares into blackSquares.txt file
# fill acrossWords list in order to write acrossWords.txt file
###
cells = soup.find_all('g', {'data-group': 'cells'})
g_cells = cells[0].find_all('g')
blackSquares = []
acrossWords = []
acrossWord = ""
acrossSquares = []
downSquares = []
for cell in g_cells:
	rect = cell.find('rect')
	# rect['class'] returns a list
	if rect['class'][0] == "Cell-block--1oNaD":
		blackId = rect['id']
		if blackId[len(blackId) - 2] == '-':
			blackSquares.append(blackId[len(blackId) - 1])
		else:
			blackSquares.append(blackId[len(blackId) - 2 : ])

	# if its not a black square, add char to the acrossWord.
	else:
		char = cell.find('text', {'text-anchor' : 'middle'}).get_text()		
		acrossWord = acrossWord + char[0]



	# reset the acrossWord if we are done with the row.
	# if the last character of id is 4 or 9, we must be done with the row. cell-id-24 etc.
	if rect['id'][-1] == '4' or rect['id'][-1] == '9':		
		acrossWords.append(acrossWord)
		acrossWord = ""

	# fill downSquareNumbers list
	# fill acrossSquareNumbers list
	text = cell.find_all('text')
	if len(text) == 4:
		if text[0].get_text() in acrossNumbers:
			if rect['id'][len(rect['id']) - 2 : len(rect['id']) - 1] == '-': 
				acrossSquares.append( (int(text[0].get_text()) , rect['id'][-1] ) ) 
			else:
				acrossSquares.append( (int(text[0].get_text()) , rect['id'][len(rect['id']) - 2 : ]) )				

		if text[0].get_text() in downNumbers:
			if rect['id'][len(rect['id']) - 2 : len(rect['id']) - 1] == '-':
				downSquares.append( (int(text[0].get_text()) , rect['id'][-1]) )
			else:
				downSquares.append( (int(text[0].get_text()) , rect['id'][len(rect['id']) - 2 : ] ) )
###
# get the down words to the downWords list.
###
downWords = []
downWord = ""
for i in range(5):
	rect1 = g_cells[i + 0].find('rect')
	rect2 = g_cells[i + 5].find('rect')
	rect3 = g_cells[i + 10].find('rect')
	rect4 = g_cells[i + 15].find('rect')
	rect5 = g_cells[i + 20].find('rect')

	if rect1['class'][0] == "Cell-block--1oNaD":
		char1 = ""
	else:
		char1 = g_cells[i + 0].find('text', {'text-anchor' : 'middle'}).get_text()[0]

	if rect2['class'][0] == "Cell-block--1oNaD":
		char2 = ""
	else:
		char2 = g_cells[i + 5].find('text', {'text-anchor' : 'middle'}).get_text()[0]

	if rect3['class'][0] == "Cell-block--1oNaD":
		char3 = ""
	else:
		char3 = g_cells[i + 10].find('text', {'text-anchor' : 'middle'}).get_text()[0]

	if rect4['class'][0] == "Cell-block--1oNaD":
		char4 = ""
	else:
		char4 = g_cells[i + 15].find('text', {'text-anchor' : 'middle'}).get_text()[0]

	if rect5['class'][0] == "Cell-block--1oNaD":
		char5 = ""
	else:
		char5 = g_cells[i + 20].find('text', {'text-anchor' : 'middle'}).get_text()[0]

	downWord = char1 + char2 + char3 + char4 + char5
	downWords.append(downWord)
	downWord = ""


time.sleep(1)
driver.close()
sorted(downSquares, key=itemgetter(0))
sorted(acrossSquares, key=itemgetter(0))
# puzzle characters, numbers right now doesnt show

# i have acrossWords
# i have downWords
# i have acrossSquares
# i have downSquares
# i have blackSquares
# i have acrossClues
# i have downClues
# i have date


print(downClues)
print(downSquares)

generated_across = []
generated_across_others = []
generated_down = []
generated_down_others = []

for across_word in acrossWords:
	
	generatedClue , possible_solutions = generate_clue(across_word)

	if generatedClue:
		generated_across.append(generatedClue)	

	if possible_solutions:
		generated_across_others.append(possible_solutions)

for down_word in downWords:
	
	generatedClue , possible_solutions = generate_clue(down_word)

	if generatedClue:
		generated_down.append(generatedClue)

	if possible_solutions:
		generated_down_others.append(possible_solutions)

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
	textSurf , textRect = smallText.render("GENERATED ACROSS" , True , (0,0,0)) , smallText.render("NEW ACROSS", True, (0,0,0)).get_rect()
	textRect.center = ( (x + 60) , (y) )
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
	textSurf , textRect = smallText.render("GENERATED DOWN" , True , (0,0,0)) , smallText.render("NEW DOWN", True, (0,0,0)).get_rect()
	textRect.center = ( (x + 50) , (y) )
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
				clues = generated_across_others[0]
				rand = random.randint(0, len(clues) -1)
				newClue = clues[rand]
				generated_across = [newClue, generated_across[1], generated_across[2], generated_across[3], generated_across[4]]
		if x_pos > 720-520 and x_pos < 750-520:
			if y_pos > 880 and y_pos < 900:
				# change across 2 clue
				clues = generated_across_others[1]
				rand = random.randint(0, len(clues) -1)
				newClue = clues[rand]
				generated_across = [generated_across[0], newClue, generated_across[2], generated_across[3], generated_across[4]]
		if x_pos > 770-520 and x_pos < 800-520:
			if y_pos > 880 and y_pos < 900:
				# change across 3 clue
				clues = generated_across_others[2]
				rand = random.randint(0, len(clues) -1)
				newClue = clues[rand]
				generated_across = [generated_across[0], generated_across[1], newClue, generated_across[3], generated_across[4]]
		if x_pos > 820-520 and x_pos < 850-520:
			if y_pos > 880 and y_pos < 900:
				# change across 4 clue
				clues = generated_across_others[3]
				rand = random.randint(0, len(clues) -1)
				newClue = clues[rand]
				generated_across = [generated_across[0], generated_across[1], generated_across[2], newClue , generated_across[4]]
		if x_pos > 870-520 and x_pos < 900-520:
			if y_pos > 880 and y_pos < 900:
				# change across 5 clue
				clues = generated_across_others[4]
				rand = random.randint(0, len(clues) -1)
				newClue = clues[rand]
				generated_across = [generated_across[0], generated_across[1], generated_across[2], generated_across[3], newClue]

		# generate generate_down
		# down
		if x_pos > 1070-670 and x_pos < 1100-670:
			if y_pos > 880 and y_pos < 900:
				# change down 1 clue
				clues = generated_down_others[0]
				rand = random.randint(0, len(clues) -1)
				newClue = clues[rand]
				generated_down = [newClue, generated_down[1], generated_down[2], generated_down[3], generated_down[4]]
		if x_pos > 1120-670 and x_pos < 1150-670:
			if y_pos > 880 and y_pos < 900:
				# change down 2 clue
				clues = generated_down_others[1]
				rand = random.randint(0, len(clues) -1)
				newClue = clues[rand]
				generated_down = [generated_down[0], newClue, generated_down[2], generated_down[3], generated_down[4]]
		if x_pos > 1170-670 and x_pos < 1200-670:
			if y_pos > 880 and y_pos < 900:
				# change down 3 clue
				clues = generated_down_others[2]
				rand = random.randint(0, len(clues) -1)
				newClue = clues[rand]
				generated_down = [generated_down[0], generated_down[1], newClue, generated_down[3], generated_down[4]]
		if x_pos > 1220-670 and x_pos < 1250-670:
			if y_pos > 880 and y_pos < 900:
				# change down 4 clue
				clues = generated_down_others[3]
				rand = random.randint(0, len(clues) -1)
				newClue = clues[rand]
				generated_down = [generated_down[0], generated_down[1], generated_down[2], newClue, generated_down[4]]
		if x_pos > 1270-670 and x_pos < 1300-670:
			if y_pos > 880 and y_pos < 900:
				# change down 5 clue
				clues = generated_down_others[4]
				rand = random.randint(0, len(clues) -1)
				newClue = clues[rand]
				generated_down = [generated_down[0], generated_down[1], generated_down[2], generated_down[3], newClue]

	showPuzzle(screen , initialX , initialY, blockSize , blackSquares , acrossWords , downWords , acrossSquares , downSquares , acrossClues , downClues , date, generated_across, generated_down)
	
	pygame.display.update()
	
	


