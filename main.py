import requests
import selectorlib
import smtplib, ssl
import os

URL="https://programmer100.pythonanywhere.com/tours/"

def scrape(url):
    """Scrape the source file for data"""
    response=requests.get(url)
    content=response.text
    return content

def extract(source):
    extractor=selectorlib.Extractor.from_yaml_file("extract.yaml")
    value=extractor.extract(source)["tours"]
    return value

def send_mail(msg):
    host = "smtp.gmail.com"
    port = 465
    username = "meetapple191@gmail.com"
    password = os.getenv("py_web")
    receiver = "meetsiddhapura@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, msg)
        print("Email sent")

def store(extracted):
    with open("data.txt","a") as file:
        file.write(extracted+"\n")

def read():
    with open("data.txt","r") as file:
        return file.read()

if __name__=="__main__":
    scraped=scrape(URL)
    extracted=extract(scraped)
    print(extracted)
    filedata=read()

    if extracted != "No upcoming tours":
        if extracted not in filedata:
            store(extracted)
            send_mail(msg="New event was found")



