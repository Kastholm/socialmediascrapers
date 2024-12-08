from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
import json
import os
import re
import sys
from datetime import date

chromedriver_bin = './chromedriver/chromedriver-windows/chromedriver.exe'
url ='https://www.instagram.com/accounts/login/?next=%2F3danmark%2F&source=desktop_nav&hl=en'
url3DK ='https://www.instagram.com/3danmark/?hl=en'
today = date.today()
index = 0

# Opret ChromeService med stien til ChromeDriver
service = webdriver.ChromeService(executable_path=chromedriver_bin)
driver = webdriver.Chrome(service=service)

#Open Tiktok
driver.get(url)
# Login
time.sleep(2)
button = driver.find_element(By.XPATH, "//button[text()='Allow all cookies']")
button.click()

time.sleep(2)

input_field = driver.find_element(By.NAME, 'username')
input_field.send_keys('Christiansen1995@live.dk')
time.sleep(2)
input_field = driver.find_element(By.NAME, 'password')
input_field.send_keys('Kastholm95')

time.sleep(1)

button = driver.find_element(By.XPATH, "//button[@type='submit']")
button.click()

time.sleep(20)

button = driver.find_element(By.XPATH, "//div[text()='Not now']")
button.click()

driver.get(url3DK)



# Start scrolling down for 5 seconds
#end_time = time.time() + 10
#while time.time() < end_time:
 #   driver.find_element("tag name", "body").send_keys(Keys.PAGE_DOWN)
  #  time.sleep(0.1)  
#time.sleep(30)
#driver.execute_script("document.body.style.zoom='20%'")
time.sleep(10)
soup = BeautifulSoup(driver.page_source, 'html.parser')
posts = driver.find_elements(By.CSS_SELECTOR, 'main > div > div:nth-child(3) > div > div div:has(a)')
videoAmount = soup.select('main > div > div:nth-child(3) > div > div div:has(a)')
print(len(videoAmount))


while index <= len(videoAmount) :
    #Click post
    time.sleep(5)
    if posts:
        print(len(posts))
        print('index', index)
        posts[index].click()
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    legit = soup.select_one('h2._a9zc:has(a[href="/3danmark/"])')
    if not legit:
        index += 1
        close = driver.find_element(By.CSS_SELECTOR, 'div.x160vmok:has(svg)')
        close.click()
        time.sleep(2)
        continue

    time.sleep(10)

    #Scrape page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(2)

    #title
    title = soup.select_one('h1._ap3a._aad7').text
    print(title)
    #published
    publishedDate = soup.select_one('time[datetime]')
    published = publishedDate['datetime'].split("T")[0]
    print(published)
    #likes
    likeAmount = soup.select_one('a.x1i10hfl > span.x193iq5w > span.html-span.x1vvkbs').text
    print('LA', likeAmount)
    #url
    postUrl = driver.current_url
    print(postUrl)
    #start JSON doc
    post = {
        "videoTitle": f"{title}",
        "url": f"{postUrl}",
        "likes": f"{likeAmount}",
        "published": f"{published}", 
        "dataFetchDate": f"{str(today)}",
        "comments": []
    }
    #Look for reply click events
    time.sleep(4)
    #article button with classes _acan _acao _acas _aj1- _ap30 which has a div and a span
    reply_sections = driver.find_elements(By.CSS_SELECTOR, 'article button:not([aria-label="Toggle audio"])._acan._acao._acas._aj1-._ap30:has(div, span)')
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
        if user.text == '3danmark':
            user = user.text if user else 'N/A'
        else:
            user = 'Anonymous'

        comment = section.select_one('ul._a9ym > div > li._a9zj div._a9zs span')
        comment = comment.text if comment else 'N/A' 

        userLikeAmount = section.select_one('ul._a9ym > div > li._a9zj div.x9f619 > span.x1lliihq > button')
        if userLikeAmount and userLikeAmount.text != 'Reply':
            userLikeAmount = userLikeAmount.text
        else:
            userLikeAmount = '0'
        print('ULA', userLikeAmount)

        timestampDate = section.select_one('ul._a9ym > div > li._a9zj time[datetime]')
        timestamp = timestampDate['datetime'].split("T")[0] if timestampDate else 'N/A'

        #print(section)
        #time.sleep(3000)
        replies = section.select('ul._a9ym > li > ul > div')
        reply_data = []
         # Iterer over alle replies og hent deres data
        if replies:
            for reply in replies:
                # Hent reply_user med fallback
                reply_user_element = reply.select_one('ul._a9ym > li > ul > div h3 div:nth-child(1) > span > div')
                if reply_user_element.text == '3danmark':
                    reply_user = reply_user_element.text if reply_user_element else 'N/A'
                else:
                     reply_user = 'Anonymous'

                # Hent reply_comment med fallback
                reply_comment_element = reply.select_one('ul._a9ym > li > ul > div span._ap3a')
                reply_comment = reply_comment_element.text if reply_comment_element else 'N/A'
                if reply_comment != 'N/A':
                    reply_comment = re.sub(r'@\w+', '', reply_comment).strip()

                reply_timestamp_element = reply.select_one('ul._a9ym > li > ul > div span time[datetime]')
                reply_timestamp = (reply_timestamp_element['datetime'].split("T")[0] if reply_timestamp_element else 'N/A')
                # Tilføj reply data til listen
                reply_data.append({
                    "user": reply_user,
                    "likes": '0',
                    "timestamp": reply_timestamp,
                    "comment": reply_comment,
                })

        # Tilføj den oprindelige kommentar og dens replies som ét objekt til data
        post['comments'].append({
            "user": user,
            "likes": userLikeAmount,
            "timestamp": timestamp,
            "comment": comment,
            "replies": reply_data  # Liste med alle svar til denne kommentar
        })

    # Konverter til JSON
    json_data = json.dumps(post, ensure_ascii=False, indent=4)
    print(json_data)
    # Lav JSON doc
    folder_name = "instaScrapes"
    os.makedirs(folder_name, exist_ok=True)
    file_path = os.path.join(folder_name, f"insta_scrape{index}.json")
    with open(file_path, "w", encoding="utf-8") as outfile:
        outfile.write(json_data)
    index += 1
    close = driver.find_element(By.CSS_SELECTOR, 'div.x160vmok:has(svg)')
    close.click()
    time.sleep(4)