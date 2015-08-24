# Time 
from time import time
big_start = time()

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Import Getpass
from getpass import getpass 

# Get facebook username and password from the user
usr = raw_input("Type your Facebook email, then press enter:")
pwd = getpass()

# Set up a new firefox profile with CSS, Image loading, and Flash disabled
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.stylesheet', 2)
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

driver = webdriver.Firefox(firefox_profile=firefox_profile)

driver.get("http://www.facebook.com")               # navigate to Facebook
elem = driver.find_element_by_id("email")           # form element containing email field
elem.send_keys(usr)
elem = driver.find_element_by_id("pass")            # form element containing password field
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)

driver.add_cookie(driver.get_cookies())             # loads call results into cookies for later navigation
driver.get("http://m.facebook.com/me")              # go to mobile version of profile

all_buttons = driver.find_elements_by_tag_name("a") # find the link that points to my friends
for bu in all_buttons:
	if bu.text == 'Friends':
		elem = bu
		break

# extract my facebook username from the link
starting_user = elem.get_attribute('href').split('/')[-1].split('?')[0]

all_friends = {}

from Queue import Queue
q = Queue()
q.put(starting_user)
crawl = True
analytics = {}

# while there are still friends to crawl
while not q.empty():
	little_start = time()

    # load the next friend to get friends of
	friends = []
	current = q.get()

    # navigate to their friends
	driver.get('http://m.facebook.com/' + current + '?v=friends')
	print 'Fetching ' + current + "'s friends..."

	batch_count = 0
	try:
		while True:
			batch_count += 1

            # add all of the friends
			batch = [tab.find_element_by_tag_name('a').get_attribute('href').split('/')[-1].split('?')[0] for tab in driver.find_element_by_id('root').find_elements_by_tag_name('table')]
			friends.extend(batch)

            # try to click the see more button, if it's not there, break, you're done with the friends
			try:
				link = driver.find_element_by_id("m_more_friends").find_element_by_tag_name('a')
				link.click()

			except:
				break
	except:
		continue

    # prevents going a level deeper (friends of friends of friends)
	if crawl:                    # if first time crawling it's the starting user
		map(q.put, friends)        # add their friends to the queue
		crawl = False              # don't do this again

	all_friends[current] = friends

	elapsed = str(time() - little_start)
	print '...Done. Took ' + elapsed + ' seconds'

	analytics[current] = {'friends' : len(friends), 'time' : elapsed, 'batch count' : batch_count}

driver.close()

import json
# write the results to results.json
out = open('results.json', 'w')
out.write(json.dumps(all_friends))
out.close()

# write the speed report to analytics.json
out = open('analytics.json', 'w')
out.write(json.dumps(analytics))
out.close()

print 'The whole process took ' + str(time() - big_start) + ' seconds'
