from re import search

import pymysql
from selenium import webdriver
import time
import datetime
import pandas as pd

from selenium.webdriver.common.by import By


def brandInput():
    # receives brandhandle from user and returns it
    print("Enter Brand Handle 1:")
    brand1 = str(input())
    return brand1


def datesInput():
    userdate = input("(YYYY-MM-DD):")
    # date1 = datetime.datetime.strptime(date1,"%d/%m/%Y").date()
    year, month, day = map(int, userdate.split('-'))
    userdate = datetime.date(year, month, day)

    return userdate


def getVideoDate():
    # retrieves publish date for video and returns it
    date_data = driver.find_elements_by_xpath('//*[@id="watch7-content"]/meta[14]')
    for i in date_data:
        date = i.get_attribute('content')
    return date


def getVideoViews():
    # retrieves video views and returns it
    view_data = driver.find_elements_by_xpath('//*[@id="watch7-content"]/meta[13]')
    for i in view_data:
        views = i.get_attribute('content')
    return views


def getVideoLikes():
    # retrieves video likes and returns
    likes = 0
    likes_data = driver.find_elements_by_xpath(
        '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div['
        '2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer['
        '1]/a/yt-formatted-string')
    for i in likes_data:
        likes = i.get_attribute('aria-label')
    return likes


def getComments():
    curr_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, " + str(curr_height) + ");")
        time.sleep(1)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if curr_height == new_height:
            break
        curr_height = new_height
    try:
        comments_data = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div['
            '1]/div/ytd-comments/ytd-item-section-renderer/div['
            '1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string/span['
            '1]')
    except:
        print("Comments disabled")
        return "0"

    comments = comments_data.text
    # print(comments)
    return comments


def getVideoTitle():
    title = ""
    title_data = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div['
                                              '1]/div/div[8]/div['
                                              '2]/ytd-video-primary-info-renderer/div/h1/yt-formatted-string')
    title = title_data.text
    return title


def getDescription():
    # Not functional -- Or necessary
    description = ""
    driver.find_element_by_xpath('/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-mealbar-promo'
                                 '-renderer/div/div[2]/ytd-button-renderer['
                                 '1]/a/tp-yt-paper-button/yt-formatted-string').click()
    time.sleep(1)
    driver.find_element_by_id('more').click()
    description_data = driver.find_element(By.ID, 'description')
    elements = description_data.find_elements(By.CLASS_NAME, 'style-scope yt-formatted-string')
    # print(len(elements))
    for i in elements:
        print(i.text)

    return description


def init():
    return 1


# Main Function
brand1 = brandInput()

print("Enter Date 1 -- ")
date1 = datesInput()
# print(date1)
print("Enter Date 2 -- ")
date2 = datesInput()
# print(date2)

driver = webdriver.Chrome(executable_path='C:\\Users\\Public\\chromedriver_win32 (1)\\chromedriver.exe')
driver.get("https://www.youtube.com/" + brand1 + "/videos")
# implement user input (brand handle) and append to string above

# add all found videos to list (added functionality to scroll through entire page 10/17/21)
links = []
# index 0 - 3 holds youtube logos, actual thumbnails start at index 4
thumbnail_links = []

# ESTABLISH CONNECTION WITH DB
server = "ls-1ef1825172e62dcc237ee491d09a0c12aff562fe.cn5ycdfnko6g.us-east-1.rds.amazonaws.com"
database_ = 'smcDB'
username = 'dbmasteruser'
password_ = 'q+o.H1sd$CRRZl&CSl>VK}-(~+t1ea&P'

db = pymysql.connect(host=server, user=username, password=password_, database=database_, charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor, port=3306)
cursor = db.cursor()

print("Database connection successfully established")
curr_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, " + str(curr_height) + ");")
    time.sleep(1)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if curr_height == new_height:
        break
    curr_height = new_height

# need to collect all dates within channel range as well
# then, if posted date may be within user timeframe, add to links list
user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
# should not need to change^ with user input
for i in user_data:
    links.append(i.get_attribute('href'))

thumbnail_data = driver.find_elements_by_xpath('//*[@id="img"]')
for i in thumbnail_data:
    thumbnail_links.append(i.get_attribute('src'))

i = init()
while True:
    if thumbnail_links[i].find("ytimg") == -1:
        thumbnail_links.pop(i)
        # print("cleaned thumbnail links at " + str(i))
        i = init()
    else:
        i += 1
    if i == 6:
        break

# print(len(thumbnail_links))
# print(len(links))
time.sleep(5)

counter = 0
t_counter = 1
while counter < len(links):
    driver.get(links[counter])
    time.sleep(2)
    date = getVideoDate()
    year, month, day = map(int, date.split('-'))
    videoDate = datetime.date(year, month, day)

    if date1 >= videoDate >= date2:
        impressions = getVideoViews()
        likes = getVideoLikes()
        comments = getComments()
        title = getVideoTitle()
        # description = getDescription()

        sql = '''
        insert into smcDB.YOUTUBE(BrandHandle,PostUrl,PostDate,PostText,Likes,Comments,Views,ImageUrl) values('%s','%s',
        '%s','%s','%s','%s','%s','%s') 
        ''' % (brand1, links[counter], videoDate, title, likes, comments, impressions, thumbnail_links[t_counter])
        cursor.execute(sql)
        db.commit()

        print("Successfully committed to database")

        time.sleep(5)

        # print("")
        # print(title)
        # print(thumbnail_links[counter])
        # print(videoDate)
        # print(impressions + " Views")
        # print(likes)
        # print(comments + " Comments")
        # print(description)
        counter += 1
        t_counter += 1
    elif videoDate < date2:
        print()
        print("Scraped all videos in range")
        driver.close()
        break
    else:
        print("Video not in date range")
        counter += 1
