import os
from splinter import Browser
from selenium import webdriver
from securid.stoken import StokenFile
import time

def get_session(url, username):
    # Remove any existing HTTP or HTTPS proxy environment variables from the os.environ dictionary
    if 'http_proxy' in os.environ or 'https_proxy' in os.environ:
        os.environ.pop('http_proxy', None)
        os.environ.pop('https_proxy', None)
    
    # Retrieve a SecurID token using the securid library
    stoken = StokenFile()
    token = stoken.get_token()

    # Create a webdriver.ChromeOptions object and set the --user-data-dir option to a specific directory
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--user-data-dir=/home/kj54321/Downloads/chrome_auto_profile')

    # Use the Browser class from the splinter library to create a new Chrome browser instance with the specified options
    with Browser('chrome', options=chrome_options) as browser:
        # Navigate to a URL using the visit method of the Browser object
        browser.visit(url)

        # Click a link on the web page that contains the text "accept this policy"
        browser.links.find_by_partial_text('accept this policy').click()

        # Find a form input element by its name attribute, fill in a username, and find another form input element by its name attribute and fill in a SecurID token code
        browser.is_text_present('username')
        #time.sleep(20)
        element = browser.find_by_name('username')
        element.fill(username)
        element = browser.find_by_name('password')
        element.fill(token.now(pin=XXXX))
        # Click a button with the value "Logon"
        browser.find_by_value('Logon').click()

        # Check if an element containing the text "Network access client components are required." is present on the page
        if browser.is_element_present_by_text("Network access client components are required.", wait_time=25):
            # If it is, retrieve the value of a cookie called MRHSession
            cookies = browser.cookies.all()
            MRHSession = cookies.get('MRHSession')
        else:
            # If the element containing the text "Network access client components are required." is not present, raise an error
            raise Exception("Oops, something went wrong.")

        # Return the value of MRHSession
        return MRHSession

if __name__ == '__main__':
    url = 'https://yourcompany.com'
    username = 'yourusername'
    session = get_session(url, username)
    print("Writing session "+session)


