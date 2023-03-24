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
import twint
from twitter_scraper import scrape_keyword
import time

string1 = "(from:elonmusk) filter:links -filter:replies"
string2 = "(from:elonmusk)"

start_time = time.time()

# scrape_keyword(keyword=string2, browser="firefox", tweets_count=100, until="2023-03-14", since="2023-02-14", output_format="csv", filename="india_2",
# proxy="66.115.38.247:5678", headless=False) #In IP:PORT format

# dict = scrape_keyword(keyword=string2,
#                browser="firefox",
#                tweets_count=100,
#                until="2023-03-14",
#                since="2023-02-14",
#                output_format="csv",
#                filename="india",
#                headless=False)
#
# print(dict)

# c = twint.Config()
# c.Username = "elonmusk"
# c.Profile = True
# c.Limit = 10
# c.Store_csv = True
# c.Output = "twint_save"
# twint.run.Search(c)

# c = twint.Config()
# c.Username = "elonmusk"
# c.Followers = True
# c.Until = "2023-03-01"
# c.Since = "2023-01-01"
# c.Limit = 100
# c.Store_csv = True
# c.Output = "twint_save/filenam_e1.csv"
# twint.run.Search(c)



# import twint
#
# c = twint.Config()
# c.Username = 'elonmusk'
# c.Until = ''
# c.Since = ''
# c.Limit = 50
# c.Store_object = True
# c.Store_csv = True
# c.Hide_output = True
# c.Output = "twint_save/data.csv"
# twint.run.Search(c)
# tweets = twint.output.tweets_list
# print("--- %s seconds ---" % (time.time() - start_time))

# c = twint.Config()
# c.Username = 'dongtran1401'
# c.Until = ''
# c.Since = ''
# c.Limit = 50
# c.Replies = False
# c.Store_object = True
# c.Hide_output = True
# twint.run.Search(c)


c = twint.Config()
c.Username = 'elonmusk'
c.Since = None
c.Until = None
c.Count = True
c.Limit = 100
c.Replies = False
c.Retweets = False
c.Store_object = True
c.Hide_output = False
twint.run.Search(c)
tweets = twint.output.tweets_list
print(tweets)


