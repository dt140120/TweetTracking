import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

# find data
def praseHTML(key, since, until, num):
    if num == 1:
        # if since == '' and until != '':
        #     url = 'https://nitter.nl/search?f=tweet&q=from%3A' + key + '%29+until%3A' + until + '+-filter%3Alinks+-filter%3Areplies&since=&until=&near='
        # elif until == '' and since != '':
        #     url = 'https://nitter.nl/search?f=tweet&q=from%3A' + key + '%29+since%3A' + since + '+-filter%3Alinks+-filter%3Areplies&since=&until=&near='
        # elif since != '' and until != '':
        url = 'https://nitter.nl/search?f=tweet&q=from%3A' + key + '%29+until%3A' + until + '+since%3A' + since + '+-filter%3Alinks+-filter%3Areplies&since=&until=&near='
    else:
        # if since == '' and until != '':
        #     url = 'https://nitter.nl/search?f=tweet&q=' + key + '%29+until%3A' + until + '+-filter%3Alinks+-filter%3Areplies&since=&until=&near='
        # elif until == '' and since != '':
        #     url = 'https://nitter.nl/search?f=tweet&q=' + key + '%29+since%3A' + since + '+-filter%3Alinks+-filter%3Areplies&since=&until=&near='
        # elif since != '' and until != '':
        url = 'https://nitter.nl/search?f=tweet&q=' + key + '%29+until%3A' + until + '+since%3A' + since + '+-filter%3Alinks+-filter%3Areplies&since=&until=&near='

    response = requests.get(url)
    object = response.content
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
                comment_span = e_status.find('div', {'class': 'icon-container'}).get_text()
                if (comment_span == ''):
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
    return result
