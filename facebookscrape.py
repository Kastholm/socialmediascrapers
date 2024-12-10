from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from lxml import etree
import requests
import time
import json
import sys
from datetime import date

chromedriver_bin = './chromedriver/chromedriver-windows/chromedriver.exe'
url ='https://www.facebook.com/3Danmark'
today = date.today()
index = 1

# Opret ChromeService med stien til ChromeDriver
service = webdriver.ChromeService(executable_path=chromedriver_bin)
driver = webdriver.Chrome(service=service)

#Open Tiktok
driver.get(url)



# Login
time.sleep(2)
button = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div')
button.click()

button = driver.find_element(By.XPATH, '/html/body')
button.click()


input_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[2]/form/div/div[3]/div/div/label/div/input')
input_field.send_keys('mac@mgdk.dk')
time.sleep(2)
input_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[2]/form/div/div[4]/div/div/label/div/input')
input_field.send_keys('')

time.sleep(1)

button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[2]/form/div/div[5]/div')
button.click()

#time.sleep(15)
#driver.execute_script("document.body.style.zoom='20%'")

time.sleep(10)
soup = BeautifulSoup(driver.page_source, 'html.parser')


while index <= 300 :

    time.sleep(10)
    # Start scrolling down for 5 seconds

    #Scrape page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(2)

    #ReadMore?
    try:
        readMoreTitle = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div/div/div/span/div[3]/div[2]/div')
        readMoreTitle.click()
    except Exception as e:
        print("Elementet blev ikke fundet:")

    #title
    dom = etree.HTML(str(soup))
    try: 
        titleEle = dom.xpath('/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div/div/div/span')
        title = titleEle[0].text
        print(title)
    except:
        title = 'Ingen titel på opslaget'
        print("No titel")

    #published
    try:
        publishedEle = dom.xpath('/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/span/div/span[1]/span/span/a')
        published = publishedEle[0].text
    except:
        published = 'Ingen udgivelsesdato'
        print('Ingen udgivelsesdato')

    #image url
    try:
        imgEle = dom.xpath('/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div/div[1]/a/div[1]/div/div/div/img')
        postUrl = imgEle[0].get('src')
    except:
        postUrl = 'intet billede'
        print('No Image')

    #likes
    try:
        likesEle = dom.xpath('/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/span/div/span[2]/span/span')
        likes = likesEle[0].text
    except:
        likes = 'Ingen likes defineret'
        print('ingen likes')

    #shares
    try:
        sharesEle = dom.xpath('/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div[2]/span/div/span/span')
        shares = sharesEle[0].text
    except:
        shares = 'Ingen shares defineret'
        print('ingen shares')

    #comments
    try:
        commentsEle = dom.xpath('/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div[1]/span/div/span/span')
        comments = commentsEle[0].text
    except:
        shares = 'Ingen comments defineret'
        print('ingen comments')

    #start JSON doc
    post = {
        "videoTitle": f"{title}",
        "url": f"{postUrl}",
        "published": f"{published}",
        "dataFetchDate": f"{str(today)}",
        "likes": f"{likes}",
        "shared": f"{shares}",
        "commentsAmount": f"{comments}",
        "comments": []
    }

    print(post)

    #Find Repliy buttons
    try:
        reply_sections = driver.find_elements(By.XPATH, '/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/span/span/div/div[4]')
        if reply_sections:
            for replyEvent in reply_sections:
                replyEvent.click()
    except:
        print('Ingen replies i denne post')

    time.sleep(8)

    # Find Replies replies buttons
    try:
        reply_reply_sections = driver.find.elements(By.XPATH, '/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div[3]/div[2]/span')
        if reply_reply_sections:
            for replyEvent in reply_reply_sections:
                replyEvent.click()
    except:
        print('Ingen reply replies i denne post')

    # Opdater soup med det nye page_source
    soup = BeautifulSoup(driver.page_source, 'html.parser')


    #Find comment sections
    # Find comment sections
    comment_sections = dom.xpath('/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[3]/div/div')
    for section in comment_sections:
        # Username
        try:
            userEle = section.xpath('.//span/a/span/span')  # Brug section.xpath() for relative søgninger
            user = userEle[0].text if userEle else 'Intet brugernavn fundet'
        except:
            user = 'Intet brugernavn fundet'
            print('no username One')

        # Comment
        try:
            commentEle = section.xpath('.//div/span/div')  # Gør det relativt til section
            comment = " ".join([ele.text for ele in commentEle if ele.text is not None]) if commentEle else 'Ingen kommentar fundet'
        except:
            comment = 'Ingen kommentar fundet'
            print('no user comment')

        # Likes
        try:
            likesEle = section.xpath('.//span/div/div[1]/span')  # Gør det relativt til section
            likes = likesEle[0].text if likesEle else 'Ingen likes'
        except:
            likes = 'Ingen likes'
            print('no likes')

        reply_data = []
        replies = section.xpath('.//div[2]/div[2]/div[1]/div[1]')  # Gør det relativt til section

        # Replies
        if replies:
            for reply in replies:
                # Username
                try:
                    reply_userEle = reply.xpath('.//span[1]/a/span/span')  # Gør det relativt til reply
                    reply_user = reply_userEle[0].text if reply_userEle else 'Intet brugernavn fundet'
                except:
                    reply_user = 'Intet brugernavn fundet'
                    print('no username Two')

                # Comment
                try:
                    reply_commentEle = reply.xpath('.//div[2]/span/div/div')  # Gør det relativt til reply
                    reply_comment = reply_commentEle[0].text if reply_commentEle else 'Ingen kommentar fundet'
                except:
                    reply_comment = 'Ingen kommentar fundet'
                    print('no user comment')

                # Likes
                try:
                    reply_likesEle = reply.xpath('.//div[2]/div[2]/div/span/div/div[1]/span')  # Gør det relativt til reply
                    reply_likes = reply_likesEle[0].text if reply_likesEle else 'Ingen likes'
                except:
                    reply_likes = 'Ingen likes'
                    print('no likes')

                # Reply replies
                reply_reply_data = []
                reply_replies = reply.xpath('.//div[1]/div[1]')  # Gør det relativt til reply
                if reply_replies:
                    for reply_reply in reply_replies:
                        try:
                            reply_reply_userEle = reply_reply.xpath('.//span/a/span/span')  # Gør det relativt til reply_reply
                            reply_reply_user = reply_reply_userEle[0].text if reply_reply_userEle else 'Intet brugernavn fundet'
                        except:
                            reply_reply_user = 'Intet brugernavn fundet'
                            print('no username Two')

                        # Comment
                        try:
                            reply_reply_commentEle = reply_reply.xpath('.//span/div/div')  # Gør det relativt til reply_reply
                            reply_reply_comment = reply_reply_commentEle[0].text if reply_reply_commentEle else 'Ingen kommentar fundet'
                        except:
                            reply_reply_comment = 'Ingen kommentar fundet'
                            print('no comment found')

                        reply_reply_data.append({
                            "user": reply_reply_user,
                            "comment": reply_reply_comment,
                        })

                # Tilføj reply data til listen
                reply_data.append({
                    "user": reply_user,
                    "comment": reply_comment,
                    "likes": reply_likes,
                    "replies": reply_reply_data
                })

        # Tilføj den oprindelige kommentar og dens replies som ét objekt til data
        post['comments'].append({
            "user": user,
            "comment": comment,
            "likes": likes,
            "replies": reply_data
        })


    # Konverter til JSON
    json_data = json.dumps(post, ensure_ascii=False, indent=4)
    # Lav JSON doc
    with open(f"facebook_scrape{index}.json", "w", encoding='utf-8') as outfile:
        outfile.write(json_data)
    index += 1
    close = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div')
    close.click()
    time.sleep(30)