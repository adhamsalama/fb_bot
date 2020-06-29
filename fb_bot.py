# Contains some Facebook related functions
# Not 100% accurate, might send messages to strangers if no friends match the name
# I'm not responsible for misuse of this script

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fb_login(driver, id, pw):
    """Logs into Facebook"""

    driver.get('https://facebook.com/')
    email = driver.find_element_by_id('email')
    email.send_keys(id)
    password = driver.find_element_by_id('pass')
    password.send_keys(pw)
    body = driver.find_element_by_tag_name('body')
    body.send_keys(Keys.ENTER)

def send_message(driver, name, message):
    """Sends a message to a friend"""

    try:
        # _58al is the search box's css class name
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_58al"))
        )
    except TimeoutException:
        raise Exception("Can't find the search box, FB might have changed its' css class")
    search = driver.find_element_by_class_name('_58al')
    search.send_keys(name)
    # _8slc is the first result's css classs name, this chooses the first result that appears, if the person isn't in your friends list it might send the message to a random person with a similar name
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_8slc"))
        )
    except TimeoutException:
        raise NameError("Friend not found")
    result = driver.find_element_by_class_name('_8slc')
    result.click()
    msg = driver.find_element_by_tag_name('body')
    msg.send_keys(message + Keys.ENTER)
    time.sleep(1)
    # Telling the friend that the message was sent by a bot, you can delete it if you want
    msg.send_keys('This message was sent by a bot.' + Keys.ENTER)
    print(f'Message "{message}"" was sent to ({name}) successfully.')

def send_spam_msg(driver, name, message, n):
    """Send a message to a friend n times"""

    for i in range(n):
        send_message(driver, name, message)

def send_msgs_to_friends(driver, names, messages, same_msg=True):
    """Sends messages to multiple friends"""

    n = len(names)
    if same_msg:
        for i in range(n):
            try:
                send_message(driver, names[i], messages)
            except NameError:
                print(f"Can't find ({names[i]})")
    else:
        for i in range(n):
            try:
                send_message(driver, names[i], messages[i])
            except NameError:
                print(f"Can't find ({names[i]})")

def get_friends(driver, username):
    """Returns a list of Facebook friends' names"""

    driver.get('https://www.facebook.com/' + username + '/friends_all')
    scroll_to_end_of_page(driver)
    friends = driver.find_elements_by_css_selector('.fsl.fwb.fcb')
    for i in range(len(friends)):
        friends[i] = friends[i].text
    return friends
    
def scroll_to_end_of_page(driver):
    """Scrolls to the bottom of the page"""

    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while match == False:
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

def main():  
    # How to send a message to a number of friends (I'm not responsible for misuse of this script)
    email = input("Email: ")
    password = input("Password: ")
    names = input("Name: ")
    # Make sure to spell correctly
    #for i in range(int(input('Number of friends: '))):
    #    names.append(input('Name: '))
    message = input("Message: ")
    driver = webdriver.Firefox()
    fb_login(driver, email, password)
    # Wait for Facebook to load completely (Sleep time depends on your internet connection)
    time.sleep(15)
    #send_msgs_to_friends(driver, names, message, same_msg=True)
    send_spam_msg(driver, names, message, 100)
    time.sleep(1)
    driver.quit()

if __name__ == "__main__":
    main()