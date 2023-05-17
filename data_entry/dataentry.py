import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import lxml
import re

DOCS_URL = 'https://forms.gle/VLWmgaxGWMUpaiF77'
RENTALS = 'https://www.zillow.com/toronto-on/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A43.91371905611492%2C%22east%22%3A-78.97469687792969%2C%22south%22%3A43.50174432370382%2C%22west%22%3A-79.77807212207031%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A792680%2C%22regionType%22%3A6%7D%5D%7D'

list_of_links= []
list_of_prices= []
list_of_addresses= []

def scrape_rentals():
    driver = uc.Chrome()
    driver.get(RENTALS)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    listings = soup.find_all('div', class_='StyledPropertyCardDataWrapper-c11n-8-85-1__sc-1omp4c3-0 jVBMsP property-card-data')
    # print(listings)
    for listing in listings:
        link = listing.find('a', class_='StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0 gdfTyO property-card-link').get("href")
        # print(link)
        list_of_links.append(link)

    for listing in listings:
        address = listing.find('address', attrs={'data-test': 'property-card-addr'})
        address_text = address.text.strip().replace('<address data-test="property-card-addr">', '').replace('</address>', '')
        # print(address_text)
        list_of_addresses.append(address_text)
    
    prices = soup.find_all('span', attrs={'data-test': 'property-card-price'})
    for price in prices:
        price_text = price.text.strip().replace('<span data-test="property-card-price">', '').replace('</span>', '').replace('C$', '').replace(',', '')
        price_value = re.findall('\d+', price_text)
        if price_value:
            list_of_prices.append(int(price_value[0]))
            # print(price_value)
        
    driver.quit()

def fill_google_doc():
    for i in range(len(list_of_links)):
        driver = uc.Chrome()
        driver.get(DOCS_URL)
        
        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/input').send_keys(list_of_addresses[i])
        driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/input').send_keys(list_of_prices[i])
        driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div[2]/div[3]/div/div[1]/input').send_keys(list_of_links[i])
        driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span').click()
        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span').click()

    

    



scrape_rentals()
print(list_of_links)
print(list_of_addresses)
print(list_of_prices)
# StyledPropertyCardDataWrapper-c11n-8-85-1__sc-1omp4c3-0 jVBMsP property-card-data
# StyledPropertyCardDataWrapper-c11n-8-85-1__sc-1omp4c3-0 jVBMsP property-card-data