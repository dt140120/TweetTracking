import json

from twitter_scraper import scrape_keyword

dict = scrape_keyword(keyword="(from:elonmusk) filter:links -filter:replies",
               browser="firefox",
               tweets_count=10,
               until="2023-03-14",
               since="2023-02-14",
               output_format="json",
               filename="",
               headless=False)

print(dict)
