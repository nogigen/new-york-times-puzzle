import urllib.request
import json
import re
from nltk.stem.lancaster import LancasterStemmer

def getDefinitionFromUrbanDictionary(word):
	print("Checking the definition and examples for word \"" +word  +"\" to generate a clue from urban dictionary.")
	st = LancasterStemmer()

	URL = "http://api.urbandictionary.com/v0/define?term="
	url = URL + word.lower()

	definitions = []
	examples = []
	definition = None
	example = None
	try:
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		content = response.read().decode('utf-8');
		contentJson = json.loads(content)

		attr = contentJson['list']
		for _attr in attr:
			definition = _attr['definition']
			example = _attr['example']

			#process definition and examples here			
			definition = re.sub("[^0-9a-zA-Z() \\-&'.,?!;:]+", '', definition)
			definition = re.sub(' +', ' ', definition)
			example = re.sub("[^0-9a-zA-Z() \\-&'.,?!;:]+", '', example)
			example = re.sub(' +', ' ', example)

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
		print("an error occured while trying to get definition and examples for the word \"" +word  +"\" from urban dictionary")	

	return definitions, examples

# print(getDefinitionFromUrbanDictionary("hah"))

