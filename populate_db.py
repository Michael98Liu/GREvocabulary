import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GREvocabulary.settings")
import django
django.setup()
from GRE import models
import json
from django.contrib.auth.models import User

fp = open("./allwords.json", "r")
allwords = json.load(fp)

with open("./definitions.json") as fd:
    definitions = json.load(fd)

    for category in allwords.keys():
        cat = models.Category(name=category)
        cat.save()
        for word in allwords[category]:
            meaning = ""
            try:
                for i, d in definitions[word].items():
                    meaning = d[0]
            except Exception as e:
                print(e)
            w = models.Word(word=word, meaning=meaning, category = cat)
            w.save()

    fp.close()

# Create an user here.
try:
    user = User.objects.create_user('yair', password = '1234')

    # Update fields and then save again
    user.first_name = 'Yair'
    user.last_name = 'Sovran'
    user.save()
    # import insert_words
except Exception as e:
    print(e)
