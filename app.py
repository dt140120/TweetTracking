import json
from flask import Flask, render_template, request
from twitter_scraper import get_profile_details

app = Flask(__name__)


# controller
def con_get_profiles(twitter_username):
    user = json.loads(get_profile_details(twitter_username=twitter_username, filename=''))
    return user

def con_get_tweets():
    return

def con_get_topics():
    return


# route
@app.route("/")
def main():
    return render_template('index.html')


@app.route("/get_profiles", methods=['GET', 'POST'])
def get_profiles():
    if request.method == 'POST':
        users = con_get_profiles(request.form.get('username'))
        # return render_template('result.html', users=users)
        return render_template('result.html')
    else:
        return render_template('profiles.html')


@app.route("/get_tweets", methods=['GET', 'POST'])
def get_tweets():
    return render_template('tweets.html')


@app.route("/get_topic", methods=['GET', 'POST'])
def get_topics():
    return render_template('topics.html')


if __name__ == "__main__":
    app.run()
