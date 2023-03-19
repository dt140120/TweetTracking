from twitter_scraper_selenium import scrape_keyword_with_api

query = "Elon Musk"
tweets_count = 10
output_filename = "gaming_hashtag_data"
scrape_keyword_with_api(query=query, tweets_count=tweets_count, output_filename=output_filename)

from twitter_scraper import scrape_keyword

scrape_keyword(keyword="(from:elonmusk) -filter:links -filter:replies",
               browser="chrome",
               tweets_count=10,
               until="2023-03-14",
               since="2023-02-14",
               output_format="csv",
               filename="india")