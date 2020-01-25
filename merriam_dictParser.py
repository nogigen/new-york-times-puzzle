import urllib.request
import json
import re
from nltk.stem.lancaster import LancasterStemmer

def getDefinitionFromMerriamDictionary(word):
	print("Checking the definition and examples for word \"" +word  +"\" to generate a clue from merriam dictionary.")

	st = LancasterStemmer()

	key = "22feffd8-d67e-4241-a3d5-66c7a021b990"
	url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" +word.lower() +"?key=" +key

	definitions = []
	examples = []
	try:
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		content = response.read().decode('utf-8');
		contentJson = json.loads(content)
		
		for el in contentJson:
			try:
				meta = el['meta']
				shortDef = el['shortdef']
				
				# process definition
				_shortDef = re.sub("[^0-9a-zA-Z() \\-&'.,?!;:]+", '', shortDef)
				_shortDef = re.sub(' +', ' ', _shortDef)
				if st.stem(word.lower()) not in _shortDef.lower():
					definitions.append(_shortDef)			

				definition = el['def']
				sseq = definition[0]["sseq"]
				dt=sseq[0][0][1]["dt"]
				example = dt[1][1][0]["t"]

				# process example
				if st.stem(word.lower()) in example:
					words = example.split(" ")
					for i in range(len(words)):
						if st.stem(word.lower()) in words[i].lower():
							words[i] = "___"
					example = " ".join(words)
					examples.append(example)

			except Exception as e:
				pass
	except Exception as e:
		print("an error occured while trying to get definition and examples for the word \"" +word  +"\" from merriam dictionary.")

	return definitions, examples

# print(getDefinitionFromMerriamDictionary("PAY UP"))
