from nltk.corpus import wordnet as wn
import random
from nltk.stem.lancaster import LancasterStemmer



def search_wordnet(word):
    st = LancasterStemmer()
    synonyms, antonyms = [], []
    definitions, examples = [], []
    hypernyms, hyponyms = [], []

    synset = wn.synsets(str(word))
    # print("\n\nSynset:", synset)
    

    for syn in synset:
        if syn.hypernyms():
            for i in range(len(syn.hypernyms())):
                hypernyms.append(syn.hypernyms()[i].name())
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

        if st.stem(word.lower()) not in syn.definition().lower():

            definitions.append(syn.definition())

        for _ex in syn.examples():
            if _ex:
                words = syn.examples()[0].split(" ")
                i = 0
                while i < len(words):
                    if st.stem(word) in words[i]:
                        words.pop(i)
                        i = i - 1
                    i = i + 1
                words = " ".join(words)
                examples.append(words)               

    return definitions, examples


    # rand = random.randint(1,100)
    # st = LancasterStemmer()

    # # 40% chance to generate a clue based on example sentences
    # # selects a random example from a random synset of the word
    # # and replaces the word with five underscores
    # if (rand > 60):
    #     try:   
    #         example_sentence = ""
    #         # while (example_sentence == ""):
    #         example_sentence = random.choice(random.choice(examples))
    #         if st.stem(word.lower()) in example_sentence:
    #             words = example_sentence.split(" ")
    #             for i in range(len(words)):
    #                 if st.stem(word.lower()) in words[i].lower():
    #                     words[i] = "___"
    #             example_sentence = " ".join(words)

    #         example_sentence = str(example_sentence[0]).upper() + str(example_sentence)[1:]
    #     except Exception as e:
    #         example_sentence = None

    #     return example_sentence
    # # 40% chance to generate a clue based on the wordnet dictionary definitions
    # elif (rand > 10):
    #     try:
    #         definition = random.choice(definitions)
    #         if st.stem(word.lower()) in definition:
    #             definition = str(definition[0]).upper() + str(definition)[1:]
    #         else:
    #             definition = None
    #     except Exception as e:
    #         definition = None
    #     return definition
        
    # # 20% chance to generate a clue from the words hypernym (parent node in 
    # # the semantic next
    # else:
    #     try:
    #         hypernym_clue = str(random.choice(hypernyms)).split(".")[0]
    #         hypernym_clue = hypernym_clue.replace("_", " ")
    #         boolean = True
    #     except Exception as e:
    #         boolean = False
    #     if boolean:
    #         return "A type of " + str(hypernym_clue)
    #     else:
    #         return None

    # # print("\nWord:", word)
    # print("\nSynonyms:", synonyms )
    # print("\nAntonyms:", antonyms)
    # print("\nDefinitions", definitions)
    # print("\nExamples: ", examples)
    # print("\nHypernyms: ", hypernyms)
    # # print("\nHyponyms: ", hyponyms)


# print(search_wordnet("NANCY"))