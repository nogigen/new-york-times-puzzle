from merriam_dictParser import getDefinitionFromMerriamDictionary
from urban_dictParser import getDefinitionFromUrbanDictionary
from wikipediaParser import wikipediaSearcher
from google_wordCorrection_and_clueGenerator import google_correction_and_clue_generator
from google_dictParser import getDefinitionFromGoogleDictionary
from wordnet_dictParser import search_wordnet

def generate_clue(word, priorityToGenerateFromDefinition=False):

	possible_definitions = []
	possible_explanations = []
	possible_solutions = []	

	# length = len(word)
	# permutations_of_word = []
	# for i in range(length):
	# 	if i == 0:
	# 		permutations_of_word.append(word)
	# 	elif i != 0 or i != length - 1:
	# 		_word = word[0:i] +" " +word[i:]
	# 		permutations_of_word.append(_word)
	# print("permutations of this word (incase its needed): ")
	# print(permutations_of_word)

	# generatedClue = None

	# for permutation in permutations_of_word:
	# 	_permutation = permutation.split(" ")
	# 	popped = False
	# 	if _permutation[0].lower() == "a" or _permutation[0].lower() == "an":
	# 		_permutation.pop(0)
	# 		popped = True
	# 	permutation = " ".join(_permutation)

	# 	if generatedClue or possible_solutions:
	# 		break	

	
			
	# wordnet
	definitions, examples = search_wordnet(word)
	if definitions:
		for _def in definitions:
			possible_definitions.append(_def)
			possible_solutions.append(_def)
	if examples:
		for _ex in examples:
			possible_solutions.append(_ex)

	# merriam dict
	merriamDictAdded = False
	for i in range(3):
		if merriamDictAdded:
			break
		definition, example = getDefinitionFromMerriamDictionary(word)
		if definition:
			for _def in definition:
				possible_definitions.append(_def)
				possible_solutions.append(_def)
				merriamDictAdded = True
		if example:
			for _ex in example:
				possible_explanations.append(_ex)
				possible_solutions.append(_ex)
				merriamDictAdded = True

	# google dict
	googleDictAdded = False
	for i in range(3):
		if googleDictAdded:
			break
		definition, example = getDefinitionFromGoogleDictionary(word)
		if definition:
			for _def in definition:
				possible_definitions.append(_def)
				possible_solutions.append(_def)
				googleDictAdded = True
		if example:
			for _ex in example:
				possible_explanations.append(_ex)
				possible_solutions.append(_ex)
				googleDictAdded = True
	

	# wikipedia
	definition = wikipediaSearcher(word)
	if definition:
		possible_definitions.append(definition)
		possible_solutions.append(definition)

	# urban dict
	urbanDictAdded = False
	for i in range(3):
		if urbanDictAdded:
			break
		definition, example = getDefinitionFromUrbanDictionary(word)
		if definition:
			for _def in definition:
				possible_definitions.append(_def)
				possible_solutions.append(_def)
				urbanDictAdded = True
		if example:
			for _ex in example:
				possible_explanations.append(_ex)
				possible_solutions.append(_ex)
				urbanDictAdded = True

	# google at the right side
	googleSolution = None
	googleEntered = False
	correctedWord , generatedClue = google_correction_and_clue_generator(word)
	if generatedClue:
		googleEntered = True
		googleSolution = generatedClue
		possible_solutions.append(googleSolution)


	generatedClue = None
	if priorityToGenerateFromDefinition:
		if possible_definitions:
			first_definition = possible_definitions[0]
			if len(first_definition.split(" ")) <= 13:
				generatedClue = first_definition
			else:
				shortest_index = 0
				shortest_len = len(first_definition.split(" "))
				for i in range(len(possible_definitions)):
					definition = possible_definitions[i]
					if len(definition.split(" ")) < shortest_len:
						shortest_index = i
						shortest_len = len(definition.split(" "))
				generatedClue = possible_definitions[shortest_index]
		

	# vote to generate clue.
	if possible_explanations:
		first_example = possible_explanations[0]
		if len(first_example.split(" ")) <= 13:
			generatedClue = first_example
		else:
			shortest_index = 0
			shortest_len = len(first_example.split(" "))
			for i in range(len(possible_explanations)):
				example = possible_explanations[i]
				if len(example.split(" ")) < shortest_len:
					shortest_index = i
					shortest_len = len(example.split(" "))
			generatedClue = possible_explanations[shortest_index]




		
	if googleEntered:		
		return googleSolution, possible_solutions
	else:
		if priorityToGenerateFromDefinition:
			if possible_definitions:
				# get the shortest clue
				shortest_clue_index = 0
				shortest_clue_len = len(possible_definitions[0].split(" "))
				for i in range(len(possible_definitions)):
					solution = possible_definitions[i]
					if len(solution.split(" ")) < shortest_clue_len:
						shortest_clue_index = i
						shortest_clue_len = len(solution.split(" "))
				rand_clue = possible_definitions[shortest_clue_index]
				return rand_clue, possible_solutions
			else:
				return generatedClue, possible_solutions

		else:
			if possible_explanations:
				shortest_clue_index = 0
				shortest_clue_len = len(possible_explanations[0].split(" "))
				for i in range(len(possible_explanations)):
					solution = possible_explanations[i]
					if len(solution.split(" ")) < shortest_clue_len:
						shortest_clue_index = i
						shortest_clue_len = len(solution.split(" "))
				rand_clue = possible_explanations[shortest_clue_index]
				return rand_clue, possible_solutions
			return generatedClue, possible_solutions




# print(generate_clue("hanks"))
