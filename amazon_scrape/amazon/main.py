from pprint import PrettyPrinter
import requests
from bs4 import BeautifulSoup
import lxml
import smtplib


pp = PrettyPrinter()


headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
'Accept-Language':'en-US,en;q=0.9'
}
url="https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
response = requests.get(url ,headers=headers)

soup=BeautifulSoup(response.content, 'lxml')

price=soup.find('span', class_='a-offscreen')
price=price.getText().split('$')
price=float(price[1])

target_price=price*0.85

title = soup.find(id="productTitle").get_text().strip()

if price < target_price:
    with smtplib.SMTP(YOUR_SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
        connection.sendmail(
            from_addr=YOUR_EMAIL,
            to_addrs=YOUR_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n"{title} is now {price}"\n{url}".encode("utf-8")
        )


