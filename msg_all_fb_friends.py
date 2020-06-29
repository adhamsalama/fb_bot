# A script that sends a message to all Facebook friends (Might not be 100% accurate)
# I'm not responsible for misuse of this script

from bot import fb_login, get_friends, send_message, scroll_to_end_of_page, webdriver
import time

def main():
    driver = webdriver.Firefox()
    email = input("Email: ")
    pw = input("Password")
    username = input("Facebook username: ")
    message = input("Message: ")
    fb_login(driver, name, pw)
    time.sleep(5)
    friends = get_friends(driver, username)
    for friend in friends:
        send_message(driver, friends[i], message)
        time.sleep(1)
    
if __name__ == "__main__":
    main()
