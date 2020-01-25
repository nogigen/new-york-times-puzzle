from bs4 import BeautifulSoup
from selenium import webdriver
import time
from googletrans import Translator
import os
from nltk.stem.lancaster import LancasterStemmer

def google_correction_and_clue_generator(word):
	correctedWord = word
	generatedClue = None
	
	try:
		print("\nChecking if the word \"" +word  +"\" is spelled correctly from google.")
		driver = webdriver.Chrome(os.getcwd() + "\\chromedriver.exe")
		url = "http://www.google.com/search?q=" +word		
		driver.get(url)
		time.sleep(1)
		soup = BeautifulSoup(driver.page_source, 'lxml')
		answerBox = soup.find('a', {'class': 'gL9Hy'})
		if answerBox:			
			correctedWord = answerBox.find('i').text
			print("google suggests a correction for the word \"" +word +"\"")
			print("it's: " +correctedWord)

	except Exception as e:
		print("Google doesn't suggest a correction for the word \"" +word +"\"")

	print("initially, the word that this program were trying to generate a clue for was \"" +word +"\"")
	print("now its \"" +correctedWord +"\"")

	try:
		resultBox = soup.find('div', {'class': 'SPZz6b'})
		divs = resultBox.find_all('div')
		result = divs[0].find('span').text
		field = divs[1].find('span').text

		translator = Translator(service_urls=['translate.google.com'])
		cluePart1 = translator.translate(result, dest="en").text.strip()
		cluePart2 = translator.translate(field, dest="en").text.strip()

		st = LancasterStemmer()

		if correctedWord.lower() in cluePart1.lower():
			words = cluePart1.split(" ")
			for i in range(len(words)):
				if st.stem(correctedWord.lower()) in words[i].lower() or corrected.lower() in words[i].lower():
					words[i] = "___"
			cluePart1 = " ".join(words)
		
		vowels = ["a", "e", "i", "o", "u"]
		if cluePart2[0].lower() in vowels:
			generatedClue = "An " + cluePart2 + " : " +cluePart1
		else:
			generatedClue = "A " + cluePart2 + " : " +cluePart1

		print("generated clue for the word \"" +word +"\" is : " +generatedClue)

		driver.close()

	except Exception as e:
		print("no google explanation with field,name,img at the right side")

	return correctedWord, generatedClue
	# or if you want to return a dictionary, return { 'word' : correctedWord, 'generatedClue': generatedClue}

# google_correction_and_clue_generator("hanks")
