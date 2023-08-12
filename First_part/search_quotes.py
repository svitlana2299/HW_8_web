import re
import redis
from models import Author, Quote
import mongoengine

# Підключення до MongoDB
mongoengine.connect(
    db='svitlana',  # Назва бази даних
    host='mongodb+srv://svitlana:JHp56XKEKjpAnMqF@atlascluster.9lwm8qe.mongodb.net/',
    alias='default'
)

# Підключення до Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def search_quotes():
    while True:
        command = input(
            "Введіть команду (name: ім'я, tag: тег, tags: теги, exit: вихід): ")

        if command == "exit":
            break

        # Розпізнавання команди за допомогою регулярних виразів
        match_name = re.match(r'name:(.*)', command)
        match_tag = re.match(r'tag:(.*)', command)
        match_tags = re.match(r'tags:(.*)', command)

        if match_name:
            author_name = match_name.group(1).strip()
            authors = Author.objects(fullname__icontains=author_name)

            if authors:
                for author in authors:
                    quotes = Quote.objects(author=author)
                    for quote in quotes:
                        print(quote.quote)
            else:
                print(f"Автор {author_name} не знайдений.")
        elif match_tag or match_tags:
            if match_tag:
                tags = [match_tag.group(1).strip()]
            elif match_tags:
                tags = [tag.strip() for tag in match_tags.group(1).split(',')]

            quotes = Quote.objects(tags__in=tags)
            for quote in quotes:
                print(quote.quote)
        else:
            print("Невідома команда. Доступні команди: name, tag, tags, exit")


if __name__ == '__main__':
    search_quotes()
