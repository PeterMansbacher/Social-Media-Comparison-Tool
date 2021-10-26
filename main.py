from selenium import webdriver
import time


def brandInput():
    # receives brandhandle from user and returns it
    print("Enter Brand Handle 1:")
    brand1 = str(input())
    return brand1


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
    likes_data = driver.find_elements_by_xpath(
        '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div['
        '2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer['
        '1]/a/yt-formatted-string')
    for i in likes_data:
        likes = i.get_attribute('aria-label')
    return likes


# Main Function
brand1 = brandInput()

driver = webdriver.Chrome(executable_path='C:\\Users\\Public\\chromedriver_win32\\chromedriver.exe')
driver.get("https://www.youtube.com/" + brand1 + "/videos")
# implement user input (brand handle) and append to string above

# add all found videos to list (added functionality to scroll through entire page 10/17/21)
links = []
# index 0 - 3 holds youtube logos, actual thumbnails start at index 4
thumbnail_links = []

curr_height = driver.execute_script("return document.documentElement.scrollHeight")
while (True):
    driver.execute_script("window.scrollTo(0, " + str(curr_height) + ");")
    time.sleep(1)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if curr_height == new_height:
        break
    curr_height = new_height

user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
# should not need to change^ with user input
for i in user_data:
    links.append(i.get_attribute('href'))

thumbnail_data = driver.find_elements_by_xpath('//*[@id="img"]')
for i in thumbnail_data:
    thumbnail_links.append(i.get_attribute('src'))

# print(len(thumbnail_links))
# print(len(links))
time.sleep(5)
driver.get(links[0])
time.sleep(5)

date = getVideoDate()
impressions = getVideoViews()
likes = getVideoLikes()

time.sleep(5)

print(thumbnail_links[4])
print(date)
print(impressions)
print(likes)
