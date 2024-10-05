import requests
import os
import smtplib
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv("C:/Python/Environmental variables/.env")
my_mail = "sampleforpythonmail@gmail.com"
password = os.getenv("smtp_app_password")
URL = "https://appbrewery.github.io/instant_pot/"

res = requests.get(URL)
data = res.content

soup = BeautifulSoup(data,"html.parser")

price = soup.find(class_="aok-offscreen").getText()
modified_price = float(price.split("$")[-1])

title = soup.find(id="productTitle",class_ = "a-size-large product-title-word-break").get_text()
formatted_title = ' '.join(title.split()).split(",")[0]

body = f"{formatted_title} is now ${modified_price}"

if modified_price < 100.00:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(my_mail, password=password)
        connection.sendmail(from_addr=my_mail,
                            to_addrs=my_mail,
                            msg=f"Subject:Price alert!!!\n\n{body}")
        print("mail sent successfully")