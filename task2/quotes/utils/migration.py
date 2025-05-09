import os
import sys
import django

import connect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes.settings")
django.setup()

from quotes_app.models import Author, Tag, Quote
from models import Author as AuthorMongo
from models import Quote as QuoteMongo


authors = AuthorMongo.objects.all()
quotes = QuoteMongo.objects.all()

for author in authors:
    Author.objects.get_or_create(
        fullname = author.fullname,
        born_date = author.born_date,
        born_location = author.born_location,
        description = author.description,
    )

for quote in quotes:
    author = Author.objects.get(fullname=quote.author.fullname)

    q, _ = Quote.objects.get_or_create(
        quote = quote.quote,
        author = author
    )

    tags = []
    for tag in quote.tags:
        t, _ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    for tag in tags:
        q.tags.add(tag)