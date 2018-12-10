import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GREvocabulary.settings")
import django
django.setup()
from GRE import models
import json

fp = open("./allwords.json", "r")
allwords = json.load(fp)
for category in allwords.keys():
    cat = models.Category(name=category)
    cat.save()
    for word in allwords[category]:
        w = models.Word(word=word, meaning="", category = cat)
        w.save()

fp.close()
