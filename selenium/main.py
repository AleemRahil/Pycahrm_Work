import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver

# list =[]
driver = uc.Chrome()
# driver.get('https://www.python.org/')
# price = driver.find_element(By.XPATH, '//*[@id="content"]/div/section/div[2]/div[2]/div/ul')
# price_list = price.text.split('\n')
# event_times = price_list[::2]
# event_names = price_list[1::2]
# events ={}
# for item in range(0, len(price_list)//2):
#     events[item] = {
#         'time': event_times[item],
#         'name': event_names[item]
#     }

# print(events)


# # while(True):
# #     pass

TIMEOUT_DURATION = 60 * 0.5   # Seconds
VERIFICATION = 5        # Seconds

driver.get('http://orteil.dashnet.org/experiments/cookie/')
cookie = driver.find_element(By.ID, 'cookie')



timeout = time.time() + VERIFICATION
five_min = time.time() + TIMEOUT_DURATION

store_list = driver.find_elements(By.CSS_SELECTOR, '#store div')
cart_ids = [item.get_attribute('id') for item in store_list]

while True:
    cookie.click()

    if time.time() > timeout:

        item_price_list = driver.find_elements(By.CSS_SELECTOR, '#store b')
        prices = [int(item.text.split('-')[1].strip().replace(',','')) for item in item_price_list if item.text != '']
        # print(item_price_list)
        cookie_upgrades = {}
        for n in range(len(cart_ids)-1):
            cookie_upgrades[prices[n]] = cart_ids[n]

        coins = driver.find_element(By.ID, 'money').text
        if ',' in coins:
            coins = coins.replace(',','')
        money=int(coins)

        affordable_upgrades = {}
        for price, id in cookie_upgrades.items():
            if money > price:
                affordable_upgrades[price] = id

        highest_affordable_upgrade = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_affordable_upgrade]


        driver.find_element(By.ID, to_purchase_id).click()

        timeout=time.time()+VERIFICATION

    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        print(cookie_per_s)
        break