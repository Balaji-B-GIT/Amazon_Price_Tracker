import requests
import os
import smtplib
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv("C:/Python/Environmental variables/.env")
my_mail = "sampleforpythonmail@gmail.com"
password = os.getenv("smtp_app_password")
URL = "https://www.amazon.in/dp/B0CGCZTYH2/ref=twister_B0CVQ9K5ZL?_encoding=UTF8&th=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "Accept-Language": "en-US,en"
}

res = requests.get(URL,headers=headers)
data = res.content

soup = BeautifulSoup(data,"html.parser")

# price = soup.find(class_="a-price-whole")
# print(price.getText())

price_data = soup.find(class_="aok-offscreen").getText()
indian_price = price_data.split(" ")[3]
modified_price = float(indian_price.split("₹")[1].replace(",",""))

title = soup.find(id="productTitle",class_ = "a-size-large product-title-word-break").get_text()
formatted_title = ' '.join(title.split())

body = f"{formatted_title} is now available for INR {modified_price}\nBuy link: {URL}"

if modified_price < 3000.00:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(my_mail, password=password)
        connection.sendmail(from_addr=my_mail,
                            to_addrs=my_mail,
                            msg=f"Subject:Price alert!!!\n\n{body}")
        print("mail sent successfully")


# We can make this code run daily at a specific time using PYTHONANYWHERE...