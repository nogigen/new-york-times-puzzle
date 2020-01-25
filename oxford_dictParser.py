import requests
import json
# not working.
def getDefinitionFromOxford(word):
	print("Checking the definition and examples for word \"" +word  +"\" to generate a clue from oxford dictionary.")

	app_id = 'e084f442'
	app_key = 'b4d1398f21624cb223a1398928c9f6c68'
	language = "en-gb"
	url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word.lower()

	definitions = []
	examples = []

	try:
		r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})		
		contentJson = json.loads(r.text)

		for results in contentJson['results']:
			lexicalEntries = result['lexicalEntries']
			for lexEntry in lexicalEntries:
				entries = lexEntry['entries']

				for _entries in entries:
					senses = _entries['senses']
					for sense in senses:
						definition = sense['definitions']
						shortDefinition = sense['shortDefinitions']
						example = sense['examples']

						definitions.append(definition)
						definitions.append(shortDefinition)
						examples.append(example)
	except Exception as e:
		print("an error occured while trying to get definition and examples for the word \"" +word  +"\" from oxford dictionary")
		

	return definitions, examples

print(getDefinitionFromOxford("art"))


