import json
from twitter_scraper import get_profile_details

twitter_username = "dongtran1401"
dict = json.loads(get_profile_details(twitter_username=twitter_username, filename=''))
print(type(dict))