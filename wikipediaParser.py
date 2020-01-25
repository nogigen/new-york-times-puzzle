import wikipedia
from nltk.tokenize import sent_tokenize
import warnings
from nltk.stem.lancaster import LancasterStemmer

def wikipediaSearcher(word):
	warnings.filterwarnings('ignore')
	st = LancasterStemmer()

	first_sentence = None
	try:
		print("\nChecking the word \"" +word  +"\" to generate a clue from wikipedia.")
		sentences = []
		summary_sentences = sent_tokenize(wikipedia.summary(word.lower()))		
		for sentence in summary_sentences:
			if word.lower() in sentence.lower():
				sentences.append(sentence)
		first_sentence = sentences[0]
		forms = ["is", "was", "are", "were"]
		forms_found = []
		which_form = []
		for form in forms:
			if form in first_sentence:
				index = first_sentence.find(form)
				which_form.append(form)
				forms_found.append(index)
		firstFormIndex = min(forms_found)
		firstForm = which_form[forms_found.index(min(forms_found))]
		first_sentence = first_sentence[firstFormIndex + len(firstForm) : ].strip()

		if st.stem(word.lower()) in first_sentence.lower():
			first_sentence = None
		
	except Exception as e:
		print("couldnt access the wikipedia page.")

	return first_sentence



# print(wikipediaSearcher("art"))