import csv
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from bs4.element import Tag

# response = requests.get('https://nitter.nl/search?f=tweet&q=coin%29+until%3A2023-02-01+since%3A2023-01-01+-filter%3Alinks+-filter%3Areplies&since=&until=&near=')
response = requests.get('https://nitter.nl/search?f=tweets&q=bitcoin+until%3A2023-01-02+since%3A2023-01-01+-filter%3Alinks+-filter%3Areplies&since=&until=&near=')
# response = requests.get('https://nitter.nl/search?f=tweets&q=%28from%3Adongtran1401%29+until%3A2023-05-01+since%3A2023-01-01+-filter%3Alinks+-filter%3Areplies&since=&until=&near=')
def struct(obj):
    row = Data(obj, _type='')
    return row


def save(object):
    row = struct(object)
    with open('tweets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writer(row)




def praseHTML(object):
    soup = BeautifulSoup(object, "html5lib")
    elements = soup.find_all('div', class_='timeline-item')
    result = []
    for e in elements:
        e_id = e.find('a', 'tweet-link')
        e_name = e.find('a', class_='fullname')
        e_username = e.find('a', class_='username')
        e_date_span = e.find('span', class_='tweet-date')
        e_date = e_date_span.find('a')
        e_avatar = e.find('img', class_='avatar')
        e_content = e.find('div', class_='tweet-content')
        e_re = {
            'id': e_id['href'].split('/')[3].split('#')[0],
            'name': e_name.contents[0],
            'date': e_date.get('title'),
            'time': e_date.contents[0],
            'content': e_content.contents[0],
            'username': e_username.contents[0],
            'tweet-url': 'https://twitter.com' + e_id['href'].split('#')[0],
            'avatar': 'https://nitter.nl' + e_avatar['src']
        }
        result.append(e_re)
        for index, e_status in enumerate(e.find('div', class_="tweet-stats")):
            if isinstance(e_status, Tag):
                comment_span = e_status.find('div', {'class':'icon-container'}).get_text()
                if comment_span == '':
                    comment_span = 0
                if index == 1:
                    e_re.update({'comment': comment_span})
                elif index == 3:
                    e_re.update({'retweet': comment_span})
                elif index == 5:
                    e_re.update({'quote': comment_span})
                elif index == 7:
                    e_re.update({'heart': comment_span})
                elif index == 9:
                    e_re.update({'play': comment_span})
    # save(result)
    return result







def tweetData(t):
    date_format = "%b %d, %Y · %I:%M %p %Z"
    data = {
            "id": str(t.id),
            "conversation_id": t.id,
            "created_at": t.date,
            "date": datetime.strptime(t.date, date_format).date(),
            "time": datetime.strptime(t.date, date_format).time(),
            "timezone": '+0700',
            "user_id": t.user_id,
            "username": t.username,
            "name": t.name,
            "place": t.place,
            "tweet": t.content,
            "language": 'en',
            "mentions": t.mentions,
            "urls": t.urls,
            "photos": t.photos,
            "replies_count": int(t.comment),
            "retweets_count": int(t.retweet),
            "likes_count": int(t.heart),
            "hashtags": t.hashtags,
            "cashtags": t.cashtags,
            "link": t['tweet-url'],
            "retweet": 'False',
            "quote_url": t.quote_url,
            "video": '0',
            "thumbnail": t.thumbnail,
            "near": t.near,
            "geo": t.geo,
            "source": t.source,
            "user_rt_id": t.user_rt_id,
            "user_rt": t.user_rt,
            "retweet_id": t.retweet_id,
            "reply_to": t.reply_to,
            "retweet_date": t.retweet_date,
            "translate": t.translate,
            "trans_src": t.trans_src,
            "trans_dest": t.trans_dest,
            }
    return data

def Data(obj, _type):
    ret = tweetData(obj)
    return ret

print(type((response.content)[0]['id']))