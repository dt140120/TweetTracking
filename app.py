import json
import twint
from flask import Flask, render_template, request
from twitter_scraper import get_profile_details, scrape_keyword

app = Flask(__name__)


#finder_box_tweets
def get_data_tweets(key, tweets_count, date_from, date_to):
    c = twint.Config()
    c.Username = key
    c.Until = date_to
    c.Since = date_from
    c.Count = True
    c.Limit = tweets_count
    c.Replies = False
    c.Retweets = False
    # c.Store_object = True
    c.Store_object = True
    c.Hide_output = True
    # print('twint.output.tweets_list',len(twint.output.tweets_list))
    if len(twint.output.tweets_list) != 0:
        twint.output.tweets_list = []
    twint.run.Search(c)
    # print('twint.output.tweets_list',len(twint.output.tweets_list))
    tweets = twint.output.tweets_list
    return tweets
#finder_box_topics
def get_data_topics(key, tweets_count, date_from, date_to):
    c = twint.Config()
    c.Search = key
    c.Until = None
    c.Since = None
    c.Count = True
    c.Limit = tweets_count
    c.Replies = False
    c.Retweets = False
    c.Store_object = True
    c.Hide_output = True
    if len(twint.output.tweets_list) != 0:
        twint.output.tweets_list = []
    twint.run.Search(c)
    topics = twint.output.tweets_list
    return topics


# controller
def con_get_profiles(twitter_username):
    user = json.loads(get_profile_details(twitter_username=twitter_username, filename=''))
    return user


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
        users = con_get_profiles(request.form.get('username'))
        return render_template('result.html', users=users)
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
        tweets = con_get_tweets(key, int(tweets_count), date_from, date_to)
        # print('tweets: ',len(tweets))
        if tweets == []:
            message = 'Không có dữ liệu'
            return render_template('tweets.html', message = message)
        elif tweets != []:
            return render_template('table.html', tweets=tweets)
    else:
        return render_template('tweets.html')


@app.route("/get_topic", methods=['GET', 'POST'])
def get_topics():
    if request.method == 'POST':
        key = request.form.get('key')
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        tweets_count = request.form.get('counts')
        topics = con_get_topics(key, int(tweets_count), date_from, date_to)
        print(topics)
        if topics == []:
            message = 'Không có dữ liệu'
            return render_template('topics.html.html', message=message)
        elif topics != []:
            return render_template('table.html', tweets=topics)
    else:
        return render_template('topics.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(debug = True)
