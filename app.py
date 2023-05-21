import json
import threading
import time

from flask import Flask, render_template, request
from twitter_scraper import get_profile_details
from twitter_scraper import praseHTML
from classify.predict_class import classify
from collections import defaultdict

app = Flask(__name__)

user_o = []
list_pre_o = []
label = ["business", "entertainment", "politics", "sport", "tech"]

# frequency
def frequencies(lst):
    freq = defaultdict(int)
    for val in lst:
        freq[val] += 1
    return dict(freq)


# finder_box_tweets
def get_data_tweets(key, tweets_count, since, until):
    list_pre = []
    tweets = praseHTML(key, since, until, 1)
    start_time = time.time()
    for tweet in tweets:
        list_pre.append(label[classify(tweet['content'])])
    print('time: ' + str(time.time() - start_time))
    return tweets, list_pre


# finder_box_topics
def get_data_topics(key, tweets_count, since, until):
    list_pre = []
    topics = praseHTML(key, since, until, 2)
    start_time = time.time()
    for topic in topics:
        list_pre.append(label[classify(topic['content'])])
    print('time: ' + str(time.time() - start_time))
    return topics, list_pre


# tìm kiếm 10 bài đăng gần nhất và tiến hành phân loại
def get_rep_twe(key, tweest_count):
    re, tw = 0, 0
    global list_pre_o
    list_pre_o = []
    since = '2023-05-01'
    until = '2023-05-20'
    re_tw_s = praseHTML(key, since, until, 1)
    for re_tw in re_tw_s:
        # re += re_tw['quote']
        # tw += re_tw['retweet']
        list_pre_o.append(label[classify(re_tw['content'])])
    return list_pre_o

# lấy dữ liệu đa luồng
def multiThread(twitter_username, key, tweest_count):
    thread1 = threading.Thread(target=con_get_profiles, args=(twitter_username,))
    thread2 = threading.Thread(target=get_rep_twe, args=(key, tweest_count,))
    thread1.start()
    thread2.start()
    # Chờ cho thread kết thúc
    thread1.join()
    thread2.join()

# controller
def con_get_profiles(twitter_username):
    global user_o
    user_o = []
    user_o = json.loads(get_profile_details(twitter_username=twitter_username, filename=''))
    return user_o

# controller
def con_get_tweets(key, tweets_count, date_from, date_to):
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

# route
@app.route("/get_profiles", methods=['GET', 'POST'])
def get_profiles():
    if request.method == 'POST':
        # lấy 10 bài đăng gần nhất để đánh giá
        multiThread(request.form.get('username'), request.form.get('username'), 10)
        print('users:', str(user_o))
        print('list_pre:', str(list_pre_o))
        dict_o = frequencies(list_pre_o)
        data_array = [['Topic', 'occurs per topic']]
        for category, count in dict_o.items():
            data_array.append([category.capitalize(), count])
        print('dict:', frequencies(list_pre_o))
        print('data_array:', data_array)
        return render_template('result.html', users=user_o, data_array=data_array)
    else:
        return render_template('profiles.html')

# route
@app.route("/get_tweets", methods=['GET', 'POST'])
def get_tweets():
    if request.method == 'POST':
        key = request.form.get('key')
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        tweets_count = request.form.get('counts')
        tweets, list_pre = con_get_tweets(key, int(tweets_count), date_from, date_to)
        print(tweets)
        print(list_pre)
        if tweets == []:
            message = 'Không có dữ liệu'
            return render_template('tweets.html', message=message)
        elif tweets != []:
            return render_template('table.html', tweets=tweets, list_pre=list_pre, key=1)
    else:
        return render_template('tweets.html')

# route
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
            return render_template('table.html', tweets=topics, list_pre=list_pre, key=2)
    else:
        return render_template('topics.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(debug=True)
