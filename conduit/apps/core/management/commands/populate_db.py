from django.core.management.base import BaseCommand
from django.utils.text import slugify
from conduit.apps.articles.models import Tag, Article
from conduit.apps.profiles.models import Profile

import wikipediaapi
import random

top_nouns = [
    "time",
    "year",
    "people",
    "way",
    "day",
    "man",
    "thing",
    "woman",
    "life",
    "child",
    "world",
    "school",
    "state",
    "family",
    "student",
    "group",
    "country",
    "problem",
    "hand",
    "part",
    "place",
    "case",
    "week",
    "company",
    "system",
    "program",
    "question",
    "work",
    "government",
    "number",
    "night",
    "point",
    "home",
    "water",
    "room",
    "mother",
    "area",
    "money",
    "story",
    "fact",
    "month",
    "lot",
    "right",
    "study",
    "book",
    "eye",
    "job",
    "word",
    "business",
    "issue",
    "side",
    "kind",
    "head",
    "house",
    "service",
    "friend",
    "father",
    "power",
    "hour",
    "game",
    "line",
    "end",
    "member",
    "law",
    "car",
    "city",
    "community",
    "name",
    "",
    "president",
    "team",
    "minute",
    "idea",
    "kid",
    "body",
    "information",
    "back",
    "parent",
    "face",
    "others",
    "level",
    "office",
    "door",
    "health",
    "person",
    "art",
    "war",
    "history",
    "party",
    "result",
    "change",
    "morning",
    "reason",
    "research",
    "girl",
    "guy",
    "moment",
    "air",
    "teacher",
    "force",
    "education"
]

top_articles = [
  "Donald Trump",
  "United States",
  "Barack Obama",
  "India",
  "Elizabeth II",
  "World War II",
  "Michael Jackson",
  "United Kingdom",
  "Lady Gaga",
  "Eminem",
  "Sex",
  "Adolf Hitler",
  "Cristiano Ronaldo",
  "Game of Thrones",
  "World War I",
  "The Beatles",
  "Justin Bieber",
  "Canada",
  "Steve Jobs",
  "Freddie Mercury",
  "Kim Kardashian",
  "The Big Bang Theory",
  "List of Presidents of the United States",
  "Australia",
  "Michael Jordan",
  "Lionel Messi",
  "Stephen Hawking",
  "Dwayne Johnson",
  "Darth Vader",
  "List of highest-grossing films",
  "Taylor Swift",
  "China",
  "Star Wars",
  "Miley Cyrus",
  "Academy Awards",
  "Lil Wayne",
  "Abraham Lincoln",
  "Elon Musk",
  "Japan",
  "Germany",
  "Johnny Depp",
  "Harry Potter",
  "New York City",
  "Kobe Bryant",
  "Selena Gomez",
  "How I Met Your Mother",
  "Rihanna",
  "LeBron James",
  "Albert Einstein",
  "September 11 attack",
  "Russia",
  "The Walking Dead (TV series)",
  "Leonardo DiCaprio",
  "Kanye West",
  "Tupac Shakur",
  "Angelina Jolie",
  "John F. Kennedy",
  "COVID-19 pandemic",
  "France",
  "Chernobyl disaster",
  "Breaking Bad",
  "Joe Biden",
  "Scarlett Johansson",
  "Tom Cruise",
  "Mila Kunis",
  "Vietnam War",
  "Arnold Schwarzenegger",
  "Pablo Escobar",
  "Meghan, Duchess of Sussex",
  "Queen Victoria",
  "Jennifer Aniston",
  "Earth",
  "Ariana Grande",
  "William Shakespeare",
  "Mark Zuckerberg",
  "List of Marvel Cinematic Universe films",
  "Bill Gates",
  "Will Smith",
  "Nicki Minaj",
  "Ted Bundy",
  "Keanu Reeves",
  "Muhammad Ali",
  "Singapore",
  "Glee (TV series)",
  "Charles Manson",
  "John Cena",
  "Bruce Lee",
  "Elvis Presley",
  "Katy Perry",
  "Israel",
  "Sexual intercourse",
  "Marilyn Monroe",
  "Diana, Princess of Wales",
  "Winston Churchill",
  "Periodic Table",
  "Illuminati",
  "Prince Philip, Duke of Edinburgh",
  "Brad Pitt",
  "London",
  "Tom Brady"
]

class Command(BaseCommand):
    help = 'Creates some sample users and articiles in the db'

    def get_titles_from_categorymembers(self, categorymembers, level=0, max_level=1):
        titles = set()
        for c in categorymembers.values():
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                self.get_titles_from_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)
            elif c.ns == 0:
                titles.add(c.title)
                # print("%s: %s" % ("*" * (level + 1), c.title))
        return titles

    def print_article(self, title):
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(title)
        print("Page - Title: %s" % page_py.title)
        print("Page - Summary: %s" % page_py.summary[0:60])
        print("Page - text: %s" % page_py.text)
        print("Page - Categories: %s" % page_py.categories.keys())

    def get_unique_slug(self, title):
        slug = slugify(title)[:50]
        count = 1
        while Tag.objects.filter(slug=slug).exists():
            slug = "%s-%s" % (slug, count)
            slug = slug[len(slug)-50:]
            count += 1
        return slug

    def get_or_create_tag(self, tag):
        if Tag.objects.filter(tag=tag).exists():
            return Tag.objects.get(tag=tag)
        slug = self.get_unique_slug(tag)

        return Tag.objects.create(tag=tag, slug=slug)

    def create_article_in_db(self, title):
        print('Generating article', title)
        wiki_wiki = wikipediaapi.Wikipedia('en', timeout=20)
        page_py = wiki_wiki.page(title)
        # tags = []
        # for category in set(list(page_py.categories.keys())):
        #     print('running', category)
        #     tag = self.get_or_create_tag(category[9:])
        #     tags.append(tag)

        random_tags = []
        for i in range(0, random.randint(0,10)):
            random_tag = self.get_or_create_tag(random.choice(top_nouns))
            random_tags.append(random_tag)

        profile = Profile.objects.all().first()
        article = Article.objects.create(
            slug = slugify(page_py.title),
            title = page_py.title,
            description = page_py.summary,
            body = page_py.text,
            author=profile,
        )
        article.tags = random_tags
        article.save()

    def handle(self, *args, **kwargs):
        # wiki_wiki = wikipediaapi.Wikipedia('en')
        # cat = wiki_wiki.page("Category:Physics")
        # titles = self.get_titles_from_categorymembers(cat.categorymembers)

        # categories = set()
        # for title in titles:
        #     categor = self.print_article(title)
        #     categories.update(categor)

        # for category in categories:
        #     print(category[9:])

        for title in top_articles:
            if not Article.objects.filter(title=title).exists():
                self.create_article_in_db(title)
