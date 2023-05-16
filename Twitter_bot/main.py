import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


URL = 'https://twitter.com/i/flow/login'
URL2 = 'https://www.speedtest.net/'
USERNAME = 'sundarpichkari'
PASSWORD = 'Twitter1'


class InternetSpeedTwitterBot:


    def __init__(self) -> None:
        
        self.driver = uc.Chrome()
        
                
    def get_internet_speed(self):
        speedtest_webpage = self.driver.get(URL2)
        time.sleep(5)
        start_test=self.driver.find_element(By.CSS_SELECTOR, '.start-button a')
        start_test.click()
        time.sleep(60)
        results = self.driver.find_elements(By.CSS_SELECTOR, '.result-data-large')
        speed_down = results[0].text
        speed_up = results[1].text

        self.down = float(speed_down)
        self.up = float(speed_up)

    def tweet_at_provider(self):
        twitter_webpage = self.driver.get(URL)
        time.sleep(5)
        user = self.driver.find_element(By.CSS_SELECTOR, '.r-homxoj')
        user.send_keys(USERNAME)
        user.send_keys(Keys.ENTER)
        time.sleep(2)
        password = self.driver.find_element(By.CSS_SELECTOR, '.r-homxoj')
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)
        time.sleep(2)
        tweet1 = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a/div')
        tweet1.click()

        text = self.driver.find_element(By.CSS_SELECTOR, '.public-DraftStyleDefault-ltr')
        text.send_keys('@Bell_LetsTalk I am getting dogshit internet speed bruh')

        tweet2 = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[3]/div/div/div[2]/div/div/span/span')
        tweet2.click()

internet_speed_twitter_bot = InternetSpeedTwitterBot()

net_speed = internet_speed_twitter_bot.get_internet_speed()
if internet_speed_twitter_bot.down < 200 or internet_speed_twitter_bot.up < 200:
    internet_speed_twitter_bot.tweet_at_provider()


while True:
    pass
