import urllib.request
import json
import unicodedata
import random
from nltk.stem.lancaster import LancasterStemmer

def getDefinitionFromGoogleDictionary(word):
	print("\nChecking the definition and examples for word \"" +word  +"\" to generate a clue from an unofficial google dictionary API.")
	st = LancasterStemmer()

	URL = 'https://googledictionaryapi.eu-gb.mybluemix.net/'
	word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf8')
	url = URL + '?define=' + word + '&lang=en'

	definition = None
	example = None
	definitions = []
	examples = []
	try:
		req = urllib.request.Request(url)
		response = urllib.request.urlopen(req)
		content = response.read().decode('utf-8')
		contentJson = json.loads(content)

		
		definition = None
		example = None
		for res in contentJson:
			definition = res['meaning']
			for key in definition.keys():
				for _definition in definition[key]:
					definition = _definition['definition']
					example = _definition['example']

					#process examples
					if st.stem(word.lower()) in example.lower():
						words = example.split(" ")
						for i in range(len(words)):
							if st.stem(word.lower()) in words[i].lower():
								words[i] = "___"
						example = " ".join(words)

						examples.append(example)

					#process definition
					if st.stem(word.lower()) in definition.lower():
						continue

					definitions.append(definition)

		# process definitions
		if definitions:
			shortest_index = 0
			shortlest_len = len(definitions[0].split(" "))
			if shortlest_len <= 13:
				definition = definitions[0]
			else:				
				for i in range(len(definitions)):
					definition = definitions[i]
					if len(definition.split(" ")) < shortlest_len:
						shortest_index = i
			definition = definitions[shortest_index]

		# process examples
		if examples:
			shortest_index = 0
			shortlest_len = len(examples[0].split(" "))
			if shortlest_len <= 13:
				example = examples[0]
			else:				
				for i in range(len(examples)):
					example = examples[i]
					if len(example.split(" ")) < shortlest_len:
						shortest_index = i
			example = examples[shortest_index]

	except Exception as e:
		print("an error occured while trying to get definition and examples for the word \"" +word  +"\" from the unofficial google dictionary API")

	return definitions, examples

# print(getDefinitionFromGoogleDictionary("PAY UP"))
