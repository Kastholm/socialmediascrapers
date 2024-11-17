from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
import json
import sys
from datetime import date

chromedriver_bin = './chromedriver/chromedriver-windows/chromedriver.exe'
url ='https://www.facebook.com/3Danmark'
today = date.today()
index = 0

# Opret ChromeService med stien til ChromeDriver
service = webdriver.ChromeService(executable_path=chromedriver_bin)
driver = webdriver.Chrome(service=service)

#Open Tiktok
driver.get(url)
# Login
time.sleep(2)
button = driver.find_element(By.XPATH, "//span[text()='Tillad alle cookies']")
button.click()

time.sleep(2)

input_field = driver.find_element(By.NAME, 'email')
input_field.send_keys('mac@mgdk.dk')
time.sleep(2)
input_field = driver.find_element(By.NAME, 'pass')
input_field.send_keys('')

time.sleep(1)

button = driver.find_element(By.CSS_SELECTOR, '//div[aria-label="Accessible login button"]')
button.click()

time.sleep(30)

# Start scrolling down for 5 seconds
#end_time = time.time() + 10
#while time.time() < end_time:
 #   driver.find_element("tag name", "body").send_keys(Keys.PAGE_DOWN)
  #  time.sleep(0.1)  
time.sleep(30)
driver.execute_script("document.body.style.zoom='20%'")
time.sleep(30)
soup = BeautifulSoup(driver.page_source, 'html.parser')
posts = driver.find_elements(By.CSS_SELECTOR, '/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div/div/div[1]/div/div[2]/div[2]/span/div/span/span')
videoAmount = soup.select('/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div/div/div[1]/div/div[2]/div[2]/span/div/span/span')
print(len(videoAmount))


while index <= len(videoAmount) :
    #Click post
    time.sleep(5)
    if posts:
        print(len(posts))
        print('index', index)
        posts[index].click()
    #time.sleep(3)
    #soup = BeautifulSoup(driver.page_source, 'html.parser')
    #legit = soup.select_one('h2._a9zc:has(a[href="/3danmark/"])')
    #if not legit:
    #    index += 1
    #    close = driver.find_element(By.CSS_SELECTOR, 'div.x160vmok:has(svg)')
    #    close.click()
    #    time.sleep(2)
    #    continue

    time.sleep(10)
    # Start scrolling down for 5 seconds
    end_time = time.time() + 10
    while time.time() < end_time:
       driver.find_element("/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div").send_keys(Keys.PAGE_DOWN)
       time.sleep(0.1)  

    #Scrape page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(2)

    #title
    title = soup.find('/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div/div/div/span').text
    print(title)
    #published
    published = soup.select_one('/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/span/div/span[1]/span/span/a')
    print(published)
    #url
    postUrl = driver.current_url
    print(postUrl)
    #start JSON doc
    post = {
        "videoTitle": f"{title}",
        "url": f"{postUrl}",
        "published": f"{published}",
        "dataFetchDate": f"{str(today)}",
        "comments": []
    }
    #Look for reply click events
    time.sleep(4)
    #article button with classes _acan _acao _acas _aj1- _ap30 which has a div and a span
    reply_sections = driver.find_elements(By.CSS_SELECTOR, '/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/span/span/div/div[4]')
# alle svar /html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div[3]/div[2]    
    if reply_sections:
        for replyEvent in reply_sections:
            replyEvent.send_keys(Keys.ENTER)
    time.sleep(15)

    # Opdater soup med det nye page_source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #select all comments
    
    comment_sections = soup.select('ul._a9ym')
    for section in comment_sections:
        #For hver kommentar henter vi 3 stykker information:
        user = section.select_one('ul._a9ym > div > li._a9zj h3 > div > span > div > a')
        user = user.text if user else 'N/A' 

        comment = section.select_one('ul._a9ym > div > li._a9zj div._a9zs span')
        comment = comment.text if comment else 'N/A' 

        timestampDate = section.select_one('ul._a9ym > div > li._a9zj time[datetime]')
        timestamp = timestampDate['datetime'].split("T")[0] if timestampDate else 'N/A'

        print(section)

        replies = section.select('ul._a9ym > li > ul > div')
        reply_data = []
         # Iterer over alle replies og hent deres data
        if replies:
            for reply in replies:
                # Hent reply_user med fallback
                reply_user_element = reply.select_one('ul._a9ym > li > ul > div h3')
                reply_user = reply_user_element.text if reply_user_element else 'N/A'

                # Hent reply_comment med fallback
                reply_comment_element = reply.select_one('ul._a9ym > li > ul > div span._ap3a')
                reply_comment = reply_comment_element.text if reply_comment_element else 'N/A'

                reply_timestamp_element = reply.select_one('ul._a9ym > li > ul > div span time[datetime]')
                reply_timestamp = (reply_timestamp_element['datetime'].split("T")[0] if reply_timestamp_element else 'N/A')
                # Tilføj reply data til listen
                reply_data.append({
                    "user": reply_user,
                    "comment": reply_comment,
                    "timestamp": reply_timestamp
                })

        # Tilføj den oprindelige kommentar og dens replies som ét objekt til data
        post['comments'].append({
            "user": user,
            "comment": comment,
            "timestamp": timestamp,
            "replies": reply_data  # Liste med alle svar til denne kommentar
        })

    # Konverter til JSON
    json_data = json.dumps(post, ensure_ascii=False, indent=4)
    print(json_data)
    # Lav JSON doc
    with open(f"insta_scrape{index}.json", "w", encoding='utf-8') as outfile:
        outfile.write(json_data)
    index += 1
    close = driver.find_element(By.CSS_SELECTOR, 'div.x160vmok:has(svg)')
    close.click()
    time.sleep(4)


