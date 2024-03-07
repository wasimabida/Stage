from selenium import webdriver 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_facebook_posts_with_hashtag(email, password, hashtag):
    browser = webdriver.Chrome() # with no path so it will search for the driver automatically

    # Open the webpage
    browser.get('https://mbasic.facebook.com/')

    # Wait for the username input field to be clickable
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    # Find the username and password input fields
    username = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password_field = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

    # Clear existing text and enter the username and password
    username.clear()
    username.send_keys(email)
    password_field.clear()
    password_field.send_keys(password)

    # Find and click the login button
    login_btn = browser.find_element("xpath", '//*[@id="login_form"]/ul/li[3]/input')
    login_btn.click()

    # Search for the input field to enter the desired hashtag
    search = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='query']")))

    # Clear existing text and enter the desired hashtag
    search.clear()
    search.send_keys(hashtag)

    # Find and click the search button
    search_btn = browser.find_element("xpath", '//*[@id="header"]/form/table/tbody/tr/td[3]/input')
    search_btn.click()

    # Wait for the posts to load
    try:
        posts = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]')))
    except TimeoutException:
        print("Posts did not load within the specified time.")
        return []

    # Find all links containing "Actualité intégrale"
    try:
        links = posts.find_elements(By.XPATH, '//a[contains(text(), "Actualité intégrale")]')
    except NoSuchElementException:
        print("No links containing 'Actualité intégrale' found.")
        return []

    # List to store extracted publications
    pubs = []

    for link in links:
        pub = {}
        
        try:
            # Get the href attribute of the link
            href = link.get_attribute('href')
            
            # Open the link in a new tab
            browser.execute_script(f"window.open('{href}', '_blank');")
            
            # Switch to the newly opened tab
            browser.switch_to.window(browser.window_handles[-1])
            
            # Get the HTML source of the new tab
            page_content = browser.page_source
            
            # Close the tab
            browser.close()
            
            # Switch back to the main tab
            browser.switch_to.window(browser.window_handles[0])
            
            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Get post text
            paragraphs = soup.find_all('p')
            pub['text'] = '\n'.join(paragraph.text for paragraph in paragraphs)
            
            pubs.append(pub)
        except Exception as e:
            print(f"An error occurred: {e}")

    return pubs
