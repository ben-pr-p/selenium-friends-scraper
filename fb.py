import requests
from bs4 import BeautifulSoup

class FB_Scraper():
  def __init__(self, cookies):
    self.s = requests.Session()
    self.cookies = cookies
    r = requests.get('https://m.facebook.com/me', cookies = self.cookies)
    self.username = r.url.split('/')[-1].split('?')[0]

  def get_friends_of(self, username):
    startidx = 0
    friends = []
    done = False

    while not done:
        r = requests.get('https://m.facebook.com/' + username + '?v=friends&startindex=' + str(startidx), cookies=self.cookies)
        new_friends = extract_friends(r.text)
        friends += new_friends
        startidx += len(new_friends)
        done = len(new_friends) == 0

    return f7(filter(lambda f: f != username, friends))


def extract_friends(raw_html):
    content = BeautifulSoup(raw_html).find('div', {"id": "root"})
    links = content.find_all("a")

    friends = []

    for l in links:
        href = l['href']
        username = href[1:].split('?')[0]
        if not ('.php' in username or '/' in username):
            friends.append(username)

    return friends

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]
