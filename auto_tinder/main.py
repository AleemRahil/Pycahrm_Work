import undetected_chromedriver as uc
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

driver = uc.Chrome()
URL_TINDER = 'https://tinder.onelink.me/9K8a/3d4abb81'
FB_EMAIL = 'projects.with.pycharm@gmail.com'
FB_PASS = 'Tinder@1'

tinder_login = driver.get(URL_TINDER)
time.sleep(2)
login_with_fb = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div/div[1]/div/div/div[3]/span/div[2]/button/div[2]/div[2]/div/div')
login_with_fb.click()
time.sleep(5)

base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)

user = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/form/div/div[1]/div/input')
user.send_keys(FB_EMAIL)
pw = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/form/div/div[2]/div/input')
pw.send_keys(FB_PASS)
pw.send_keys(Keys.ENTER)

driver.switch_to.window(base_window)
print(driver.title)

#Delay by 5 seconds to allow page to load.
time.sleep(5)

#Allow location
allow_location_button = driver.find_element(By.XPATH,'/html/body/div[2]/main/div/div/div/div[3]/button[1]/div[2]/div[2]')
allow_location_button.click()
time.sleep(5)

# #Disallow notifications
notifications_button = driver.find_element(By.XPATH,'/html/body/div[2]/main/div/div/div/div[3]/button[2]/div[2]/div[2]')
notifications_button.click()
time.sleep(5)

#Allow cookies
cookies = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/button/div[2]/div[2]')
cookies.click()
time.sleep(5)








for n in range(5):
    time.sleep(5)
    try:
       
        like_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[4]/button/span/span/svg')
        like_button.click()
        
    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element(By.CSS_SELECTOR, '.itsAMatch a')
            match_popup.click()

        #Catches the cases where the "Like" button has not yet loaded, so wait 2 seconds before retrying.
        except NoSuchElementException:
            time.sleep(5)
# driver.close()

while True:
    pass