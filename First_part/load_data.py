import json
import mongoengine
from models import Author, Quote

# Налаштування підключення до бази даних
mongoengine.connect(
    db='test',  # Назва бази даних
    host='mongodb+srv://svitlana:JHp56XKEKjpAnMqF@atlascluster.9lwm8qe.mongodb.net/',
    alias='default'
)


def load_authors(filename):
    with open(filename, 'r') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            existing_author = Author.objects(
                fullname=author_data['fullname']).first()
            if not existing_author:
                author = Author(**author_data)
                author.save()


def load_quotes(filename):
    with open(filename, 'r') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            if author:
                quote_data['author'] = author
                quote = Quote(**quote_data)
                quote.save()


if __name__ == '__main__':
    load_authors('authors.json')
    load_quotes('qoutes.json')
