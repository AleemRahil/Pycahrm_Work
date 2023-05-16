import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import csv
import time


def scrape_youtube_data(url):
    driver = uc.Chrome()  # Make sure you have ChromeDriver installed and in your system PATH
    driver.get(url)

    load_all_videos(driver)

    video_titles = []
    video_views = []
    video_dates = []

    # Wait for 10 seconds to load all the videos
    time.sleep(60)
    # Find all video titles
    titles = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
    for title in titles:
        video_titles.append(title.text.strip())

    # Find all video views
    views = driver.find_elements(By.CSS_SELECTOR,
                                 'ytd-video-meta-block[rich-meta][mini-mode] #metadata-line.ytd-video-meta-block')
    for view in views:
        video_views.append(view.text.replace('\n', ' ').strip().split(' ')[0])

    for view in views:
        video_dates.append(view.text.split('\n')[-1].strip())

    # for view in views:
    #     video_dates.append(view.text.replace('\n', ' ').strip().split(' ')[1])

    driver.quit()

    return video_titles, video_views, video_dates


def load_all_videos(driver):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

def save_to_csv(titles, views, dates):
    with open('youtube_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Video Title', 'Views'])
        for i in range(len(titles) - 1):
            writer.writerow([titles[i], views[i], dates[i]])


# Example usage
youtube_url = 'https://www.youtube.com/@Friends/videos'

titles, views, dates = scrape_youtube_data(youtube_url)

save_to_csv(titles, views, dates)

# ['19 views\n6 days ago', '479 views\n1 month ago', '1.1K views\n1 month ago', '493 views\n8 months ago', '936 views\n8 months ago', '45K views\n1 year ago', '7.9K views\n1 year ago', '4.3K views\n1 year ago', '16K views\n1 year ago', '4.5K views\n1 year ago', '2.1K views\n1 year ago', '10K views\n1 year ago', '11K views\n1 year ago', '53K views\n1 year ago', '4K views\n1 year ago', '']