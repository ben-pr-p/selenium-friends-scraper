# Selenium imports
from selenium import webdriver

def login_firefox():
    # Set up a new firefox profile
    firefox_profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=firefox_profile)

    # navigate to Facebook
    driver.get("http://www.facebook.com")

    # wait for the user to enter in their password
    while True:
        try:
            loginSignifier = driver.find_element_by_class_name("innerWrap")
            break
        except:
            continue

    # get the cookies and quit
    cookies = driver.get_cookies()
    driver.quit()

    # desired format for requests library
    formatted= {}
    for cook in cookies:
        formatted[cook['name']] = cook['value']

    return formatted
