# Import libraries
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import sqlite3
import datetime
import time
import sys





        

#pakt de actuele tijd afgerond op hele minuten
dayNowInText = datetime.datetime.now().strftime("%Y-%m-%d")
timeNowInText = datetime.datetime.now().strftime("%H:%M:00")

try:
    conn = sqlite3.connect('C:\\Users\\Dave\\metingen.db')
except:
    print("error: ", sys.exc_info()[0])
    
c = conn.cursor()
#pas de range aan voor het aantal minuten dat je wil meten
for i in range(0, 615):
    #Leest de website en zoekt naar de juiste data.
    r = requests.get("https://weather.com/nl-NL/weer/vandaag/l/744c7ffd76f9b3b3915d63e2c3bdb02eda5f77c9006ea1f45d5cd9f21f6a6a41")
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    soup = soup.find_all(string=re.compile(" mb"))
    soup = soup[0].string
    soup = soup[:4]
    #print(soup)

   #Sql statements om de database in te laden. 
    query = "INSERT INTO Luchtdruk2 (Datum, Tijd, Meting) VALUES ("
    query += ("'" + dayNowInText + "','")
    query += (timeNowInText) + "','"
    query += (soup) + "')"
    
    print(query)
    
    c.execute(query)
    
    #per minuut
    time.sleep(60)
    timeNowInText = datetime.datetime.now().strftime("%H:%M:00")
   
conn.commit()
conn.close()

