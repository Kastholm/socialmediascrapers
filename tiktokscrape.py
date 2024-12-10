from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
import json
import sys
import os
from datetime import date

chromedriver_bin = './chromedriver/chromedriver-windows/chromedriver.exe'
url ='https://www.tiktok.com/@3danmark'
today = date.today()
index = 0

# Opret ChromeService med stien til ChromeDriver
service = webdriver.ChromeService(executable_path=chromedriver_bin)
driver = webdriver.Chrome(service=service)

#Open Tiktok
driver.get(url)
# Solve puzzle manually, login and zoom out
time.sleep(0)

driver.execute_script("document.body.style.zoom='20%'")

soup = BeautifulSoup(driver.page_source, 'html.parser')
videoAmount = soup.select('div[data-e2e="user-post-item"]')

while len(videoAmount) >= index:
    #Click post
    posts = driver.find_elements(By.CSS_SELECTOR, 'div[data-e2e="user-post-item"]')
    if posts:
        posts[index].click()

    #pause video
    time.sleep(10)
    pause = driver.find_element(By.CSS_SELECTOR, 'video')
    pause.click()

    #Scrape page
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #title
    title = soup.select_one('h1[data-e2e="browse-video-desc"] span:nth-child(1)').text
    #published
    published = soup.select_one('span[data-e2e="browser-nickname"] span:nth-child(3)').text
    # Likes
    likeAmount = soup.select_one('strong[data-e2e="browse-like-count"]')
    likeAmount = likeAmount.text if likeAmount else '0'
    # Comments
    commentAmount = soup.select_one('strong[data-e2e="browse-comment-count"]')
    commentAmount = commentAmount.text if commentAmount else '0'
    # Shares
    shareAmount = soup.select_one('strong[data-e2e="undefined-count"]')
    shareAmount = shareAmount.text if shareAmount else '0'
    #url
    postUrl = driver.current_url
    #time.sleep(2000)
    #start JSON doc
    post = {
        "videoTitle": f"{title}",
        "url": f"{postUrl}",
        "likes": likeAmount, 
        "commentsCount": commentAmount,  
        "sharesCount": shareAmount, 
        "published": f"{published}",
        "dataFetchDate": f"{str(today)}",
        "comments": []
    }
    #Look for reply click events
    time.sleep(4)
    reply_sections = driver.find_elements(By.CSS_SELECTOR, 'p[data-e2e="view-more-1"]')
    if reply_sections:
        for replyEvent in reply_sections:
            replyEvent.send_keys(Keys.ENTER)
    time.sleep(15)

    # Opdater soup med det nye page_source
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #select all comments
    comment_sections = soup.select('div[class*="DivCommentItemContainer"]')
    for section in comment_sections:
        #For hver kommentar henter vi 3 stykker information:
        user = 'Anonymous' #section.select_one('span[data-e2e="comment-username-1"]').text
        likes_count = section.select_one('span[data-e2e="comment-like-count"]').text
        comment = section.select_one('p[data-e2e="comment-level-1"] span').text
        timestamp = section.select_one('span[data-e2e="comment-time-1"]').text
        replies = section.select('div[class*="DivReplyContainer"] div[class*="DivCommentContentContainer"]')
        reply_data = []
         # Iterer over alle replies og hent deres data
        if replies:
            for reply in replies:
                reply_user = reply.select_one('span[data-e2e="comment-username-2"]')
                if reply_user == '3 Danmark':
                    reply_user = '3 Danmark'
                else:
                    reply_user = 'Anonymous'
                reply_likes_count = section.select_one('span[data-e2e="comment-like-count"]').text
                reply_comment = reply.select_one('p[data-e2e="comment-level-2"] span').text
                reply_timestamp = reply.select_one('span[data-e2e="comment-time-2"]').text
                # Tilføj reply data til listen
                reply_data.append({
                    "user": reply_user,
                    "likes": reply_likes_count,
                    "comment": reply_comment,
                    "timestamp": reply_timestamp
                })

        # Tilføj den oprindelige kommentar og dens replies som ét objekt til data
        post['comments'].append({
            "user": user,
            "likes": likes_count,
            "comment": comment,
            "timestamp": timestamp,
            "replies": reply_data  # Liste med alle svar til denne kommentar
        })

    # Konverter til JSON
    json_data = json.dumps(post, ensure_ascii=False, indent=4)
    print(json_data)
    # Lav JSON doc
    folder_name = "tiktokScrapes"
    os.makedirs(folder_name, exist_ok=True)
    file_path = os.path.join(folder_name, f"tiktok_scrape{index}.json")
    with open(file_path, "w", encoding="utf-8") as outfile:
        outfile.write(json_data)
    index += 1
    close = driver.find_element(By.CSS_SELECTOR, 'button[data-e2e="browse-close"]')
    close.click()
    time.sleep(10)


    
    # 1 python .\tiktokscrape.py
    # 2 Solve puzzle
    # 3 Zoom out to load posts
    # 4 Crashes after 5ish post
    # 5 Hvis den crasher hust at skift index oppe i toppen til næste video index