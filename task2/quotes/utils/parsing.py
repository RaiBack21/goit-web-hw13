import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from quotes_app.models import Author, Quote, Tag

BASE_URL = "http://quotes.toscrape.com"


def parse_data():
    page = 1
    while True:
        url = f"{BASE_URL}/page/{page}/"
        response = requests.get(url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.content, "html.parser")
        quotes = soup.find_all("div", attrs={"class": "quote"})

        if not quotes:
            break

        for quote in quotes:
            fullname = quote.find("small", attrs={"class": "author"}).text
            quote_text = quote.find("span", attrs={"class": "text"}).text
            tags = quote.find("div", attrs={"class": "tags"}).find_all(
                "a", attrs={"class": "tag"}
            )
            tag_names = [tag.text for tag in tags]
            
            try:
                author = Author.objects.get(fullname=fullname)
            except ObjectDoesNotExist as e:
                author_url = (
                    BASE_URL + quote.find(
                        "small", attrs={"class": "author"}
                        ).find_next("a")["href"]
                )
                author_resp = requests.get(author_url)
                author_soup = BeautifulSoup(author_resp.content, "html.parser")
                born_date = author_soup.find('span', attrs={'class': 'author-born-date'}).text
                born_date = datetime.strptime(born_date, "%B %d, %Y")
                born_location = author_soup.find('span', attrs={'class': 'author-born-location'}).text
                description = author_soup.find('div', attrs={'class': 'author-description'}).text

                author = Author(
                    fullname=fullname,
                    born_date = born_date,
                    born_location = born_location,
                    description = description
                )
                author.save()

            quote_obj, _ = Quote.objects.get_or_create(quote=quote_text, author=author)
            
            for tag_name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                quote_obj.tags.add(tag_obj)

        page += 1
