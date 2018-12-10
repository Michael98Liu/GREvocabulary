from PyDictionary import PyDictionary
import json

dictionary=PyDictionary()
meanings = {}

with open('./allwords.json') as f:
    allwords = json.load(f)
    with open('./definitions.json', 'w') as fw:

        for category in allwords.keys():
            for word in allwords[category]:
                definition = dictionary.meaning(word)
                meanings[word] = definition
                print(word)
        json.dump(meanings, fw)
