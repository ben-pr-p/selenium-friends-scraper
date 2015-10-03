# Import login
import login

# Import fb
from fb import FB_Scraper

# login
cookies = login.login_firefox()

scraper = FB_Scraper(cookies)

all_friends = {}

from Queue import Queue
q = Queue()
q.put(scraper.username)
crawl = True

# while there are still friends to crawl
while not q.empty():
    # load the next friend to get friends of
    current = q.get()

    # navigate to their friends
    print 'Fetching ' + current + "'s friends..."
    friends = scraper.get_friends_of(current)
    print friends

    # prevents going a level deeper (friends of friends of friends)
    if crawl:                    # if first time crawling it's the starting user
        map(q.put, friends)        # add their friends to the queue
        crawl = False              # don't do this again

    all_friends[current] = friends

import json
# write the results to results.json
out = open('results.json', 'w')
out.write(json.dumps(all_friends))
out.close()

