from newsapi import NewsApiClient
from auth import news_api_token

api = NewsApiClient(api_key=news_api_token)
response = api.get_sources()

ids = set()
names = set()
categories = set()
languages = set()
countries = set()

for source in response['sources']:
    ids.add(source['id'])
    names.add(source['name'])
    categories.add(source['category'])
    languages.add(source['language'])
    countries.add(source['country'])

print(ids)
print(names)
print(categories)
print(languages)
print(countries)
