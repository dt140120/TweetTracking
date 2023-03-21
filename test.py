import json

# from twitter_scraper import scrape_keyword
#
# dict = scrape_keyword(keyword="(from:elonmusk) filter:links -filter:replies",
#                browser="firefox",
#                tweets_count=10,
#                until="2023-03-14",
#                since="2023-02-14",
#                output_format="json",
#                filename="",
#                headless=False)
#
# print(dict)

from twitter_scraper_selenium import scrape_keyword
import time

string1 = "(from:elonmusk) filter:links -filter:replies"
string2 = "(from:elonmusk)"

start_time = time.time()

# scrape_keyword(keyword=string2, browser="firefox", tweets_count=100, until="2023-03-14", since="2023-02-14", output_format="csv", filename="india_2",
# proxy="66.115.38.247:5678", headless=False) #In IP:PORT format


dict = scrape_keyword(keyword=string2,
               browser="firefox",
               tweets_count=100,
               until="2023-03-14",
               since="2023-02-14",
               output_format="csv",
               filename="india",
               headless=False)

print(dict)

print("--- %s seconds ---" % (time.time() - start_time))


