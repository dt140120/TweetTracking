import json
import threading

import time
import twint
from flask import Flask, render_template, request
from twitter_scraper import get_profile_details
from threading import Thread
from classify.predict_class import classify
from collections import defaultdict

app = Flask(__name__)

user_o = []
list_pre_o = []
label = ["business", "entertainment", "politics", "sport", "tech"]

def frequencies(lst):
    freq = defaultdict(int)
    for val in lst:
        freq[val] += 1
    return dict(freq)

# finder_box_tweets
def get_data_tweets(key, tweets_count, date_from, date_to):
    list_pre = []
    c = twint.Config()
    # c.Username = key
    c.Search = "(from:" + key + ") -filter:links -filter:replies"
    c.Until = date_to
    c.Since = date_from
    c.Count = True
    c.Limit = tweets_count
    c.Store_object = True
    c.Hide_output = True
    if len(twint.output.tweets_list) != 0:
        twint.output.tweets_list = []
    twint.run.Search(c)
    tweets = twint.output.tweets_list
    for tweet in tweets:
        list_pre.append(label[classify(tweet.tweet)])
    return tweets, list_pre


# finder_box_topics
def get_data_topics(key, tweets_count, date_from, date_to):
    list_pre = []
    c = twint.Config()
    c.Search = key
    c.Until = None
    c.Since = None
    c.Count = True
    c.Limit = tweets_count
    c.Store_object = True
    c.Hide_output = True
    if len(twint.output.tweets_list) != 0:
        twint.output.tweets_list = []
    twint.run.Search(c)
    topics = twint.output.tweets_list
    for topic in topics:
        list_pre.append(label[classify(topic.tweet)])
    return topics, list_pre

# finder_replies_tweets_15
def get_rep_twe(key, tweest_count):
    re, tw = 0, 0
    global list_pre_o
    list_pre_o = []
    c = twint.Config()
    c.Search = "(from:" + key + ")"
    c.Count = True
    c.Limit = tweest_count
    c.Store_object = True
    c.Hide_output = True
    if len(twint.output.tweets_list) != 0:
        twint.output.tweets_list = []
    twint.run.Search(c)
    re_tw_s = twint.output.tweets_list
    for re_tw in re_tw_s:
        re += re_tw.replies_count
        tw += re_tw.retweets_count
        list_pre_o.append(classify(re_tw.tweet))
    # list_o.append(re, tw)
    return list_pre_o


def multiThread(twitter_username,key, tweest_count ):

    thread1 = threading.Thread(target=con_get_profiles, args=(twitter_username,))
    thread2 = threading.Thread(target=get_rep_twe, args=(key,tweest_count,))
    thread1.start()
    thread2.start()
    # Chờ cho thread kết thúc
    thread1.join()
    thread2.join()

    # return user, list, list_pre

# controller
def con_get_profiles(twitter_username):
    global user_o
    user_o = []
    user_o= json.loads(get_profile_details(twitter_username=twitter_username, filename=''))
    return user_o


# controller
def con_get_tweets(key, tweets_count, date_from, date_to):
    # tweets = json.loads(scrape_keyword(keyword=key, browser="firefox", tweets_count=tweets_count, until=date_to, since=date_from, output_format="json", filename="", headless=False))
    tweets = get_data_tweets(key, tweets_count, date_from, date_to)
    return tweets


# controller
def con_get_topics(key, tweets_count, date_from, date_to):
    topics = get_data_topics(key, tweets_count, date_from, date_to)
    return topics


# route
@app.route("/")
def main():
    return render_template('index.html')


@app.route("/get_profiles", methods=['GET', 'POST'])
def get_profiles():
    if request.method == 'POST':
        # users = con_get_profiles(request.form.get('username'))
        multiThread(request.form.get('username'),request.form.get('username'),15)
        # time.sleep(4)
        print('users:', str(user_o))
        print('list_pre:', str(list_pre_o))
        # re_tw = get_rep_twe(request.form.get('username'), int(15))
        print('dict:',frequencies(list_pre_o))
        return render_template('result.html', users=user_o)
    else:
        return render_template('profiles.html')


@app.route("/get_tweets", methods=['GET', 'POST'])
def get_tweets():
    if request.method == 'POST':
        key = request.form.get('key')
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        tweets_count = request.form.get('counts')
        # print('tweets_count: ',len(tweets_count))
        tweets, list_pre = con_get_tweets(key, int(tweets_count), date_from, date_to)
        print(list_pre)
        # print('tweets: ',len(tweets))
        if tweets == []:
            message = 'Không có dữ liệu'
            return render_template('tweets.html', message=message)
        elif tweets != []:
            return render_template('table.html', tweets=tweets, list_pre=list_pre)
    else:
        return render_template('tweets.html')


@app.route("/get_topic", methods=['GET', 'POST'])
def get_topics():
    if request.method == 'POST':
        key = request.form.get('key')
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        tweets_count = request.form.get('counts')
        topics, list_pre = con_get_topics(key, int(tweets_count), date_from, date_to)
        print(topics)
        print(list_pre)
        if topics == []:
            message = 'Không có dữ liệu'
            return render_template('topics.html.html', message=message)
        elif topics != []:
            return render_template('table.html', tweets=topics, list_pre=list_pre)
    else:
        return render_template('topics.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(debug=True)
