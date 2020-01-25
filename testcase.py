from clueGenerator import generate_clue
import random

from google.cloud import translate
def sample_translate_text(text, target_language, project_id):
	"""
	Translating Text

	Args:
	  text The content to translate in string format
	  target_language Required. The BCP-47 language code to use for translation.
	"""

	client = translate.TranslationServiceClient()

	# TODO(developer): Uncomment and set the following variables
	# text = 'Text you wish to translate'
	# target_language = 'fr'
	# project_id = '[Google Cloud Project ID]'
	contents = [text]
	parent = client.location_path(project_id, "global")

	response = client.translate_text(
	    parent=parent,
	    contents=contents,
	    mime_type='text/plain',  # mime types: text/plain, text/html
	    source_language_code='tr',
	    target_language_code=target_language)
	# Display the translation for each input text provided
	for translation in response.translations:
	    print(u"Translated text: {}".format(translation.translated_text))

project_id = 394028573487
text = "Ankara'da bir inşaat şirketi: Erg inşaat"
target_language = "en"

sample_translate_text(text, target_language, project_id)


# generatedClue = generate_clue("erg")
# print(generatedClue)
# clues = {
#     "across": [
#       {
#         "clue": "Pharmacy giant that acquired Aetna",
#         "answer": "CVS",
#         "number": "1"
#       },
#       {
#         "clue": "Circle or cylinder",
#         "answer": "SHAPE",
#         "number": "4"
#       },
#       {
#         "clue": "Device replaced by the cellphone",
#         "answer": "PAGER",
#         "number": "6"
#       },
#       {
#         "clue": "opposite of old",
#         "answer": "YOUNG",
#         "number": "7"
#       },
#       {
#         "clue": "\"No thanks, I'm all ___\"",
#         "answer": "SET",
#         "number": "8"
#       }
#     ],
#     "down": [
#       {
#         "clue": "Dr. Ian Malcom's theory( Jurassic Park)",
#         "answer": "CHAOS",
#         "number": "1"
#       },
#       {
#         "clue": "Hazily defined",
#         "answer": "VAGUE",
#         "number": "2"
#       },
#       {
#         "clue": "Night was young, money was ",
#         "answer": "SPENT",
#         "number": "3"
#       },
#       {
#         "clue": "Agent who is supposed to sneak into the opponents to gather information",
#         "answer": "SPY",
#         "number": "4"
#       },
#       {
#         "clue": "Unit of energy equal to 10-7 joules",
#         "answer": "ERG",
#         "number": "5"
#       }
#     ]
#   }

# accrossClues = clues['across']
# downClues = clues['down']
# a_clues = []
# d_clues = []
# for clue in accrossClues:
# 	rand = random.randint(0,9)
# 	if rand >= 4:
# 		generatedClue = generate_clue(clue['answer'].lower())
# 	else:
# 		generatedClue = generate_clue(clue['answer'].lower(), True)
# 	a_clues.append(generatedClue)

# for clue in downClues:
# 	rand = random.randint(0,0)
# 	if rand >= 4:
# 		generatedClue = generate_clue(clue['answer'].lower())
# 	else:
# 		generatedClue = generate_clue(clue['answer'].lower(), True)
# 	d_clues.append(generatedClue)

# print(a_clues)
# print("--")
# print(d_clues)
# remove top, uncomment bottom
# dont delete the modules :)

# accrossClues = ["HAHA", "OKAY","TWINE","OINK","MEDS"]
# downClues = ["TOM", "HOWIE", "AKIND", "HANKS","AYE"]
# a_clues = []
# d_clues = []
# clueFromExampleCounter = 0
# clueFromDefinitionCounter = 0
# for clue in accrossClues:
# 	rand = random.randint(0,9)
# 	if rand >= 4:
# 		generatedClue = generate_clue(clue.lower())
# 	else:
# 		generatedClue = generate_clue(clue.lower(), priorityToGenerateFromDefinition=True)

# 	if generatedClue:
# 		a_clues.append(generate_clue(clue.lower()))
# 	else:
# 		a_clues.append("couldnt find a clue.")

# for clue in downClues:
# 	rand = random.randint(0,9)
# 	if rand >= 4:
# 		generatedClue = generate_clue(clue.lower())
# 	else:
# 		generatedClue = generate_clue(clue.lower(), priorityToGenerateFromDefinition=True)

# 	if generatedClue:
# 		d_clues.append(generate_clue(clue.lower()))
# 	else:
# 		d_clues.append("couldnt find a clue.")

# print(a_clues)
# print("---")
# print(d_clues)