from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import csv
import time


def scrape_youtube_data(url):
    driver = uc.Chrome()  # Make sure you have ChromeDriver installed and in your system PATH
    driver.get(url)

    video_titles = []
    video_views = []
    time.sleep(2)
    # Find all video titles
    titles = driver.find_elements(By.XPATH,'//*[@id="video-title"]')
    for title in titles:
        video_titles.append(title.text.strip())

    # Find all video views
    views = driver.find_elements(By.CSS_SELECTOR,'ytd-video-meta-block[rich-meta][mini-mode] #metadata-line.ytd-video-meta-block')
    for view in views:
        video_views.append(view.text.replace('\n', ' ').strip().split(' ')[0])

    driver.quit()

    return video_titles, video_views

def save_to_csv(titles, views):
    with open('youtube_data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        print(titles)
        print(views)
        writer.writerow(['Video Title', 'Views'])
        for i in range(len(titles)-1):
            writer.writerow([titles[i], views[i]])

# Example usage
youtube_url = 'https://www.youtube.com/@gridrule/videos'
titles, views = scrape_youtube_data(youtube_url)

save_to_csv(titles, views)