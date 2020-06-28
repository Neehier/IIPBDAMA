import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math
import sqlite3
import datetime
import sys
from bs4 import BeautifulSoup
import requests

DO = 17
GPIO.setmode(GPIO.BCM)

try:
    conn = sqlite3.connect("/home/pi/Weerstation/Weerstation")
except:
    print("error: ", sys.exc_info()[0])

def setup():
    ADC.setup(0x48)
    GPIO.setup(DO, GPIO.IN)

def loop():
    status = 1
    tmp = 1
    while True:
        analogVal = ADC.read(0)
        Vr = 5 * float(analogVal) / 255
        Rt = 10010 * Vr / (5 - Vr)
        temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
        temp = temp - 273.15

        # 2. For Thermister module(with sig pin)
        if temp > 33:
           tmp = 0;
        elif temp < 31:
           tmp = 1;
        #################################################

        if tmp != status:
            #Print(tmp)
            status = tmp
        
        temp = "%.2f" % temp
        naarDb(temp)
        ExterneData()

        time.sleep(60)
        
def naarDb(temp):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    Time = datetime.datetime.now().strftime("%H:%M:00")
    
    query = "INSERT INTO Temperatuur (Datum, Tijd, Temperature) VALUES ("
    query += "'" + date + "','"
    query += Time + "','"
    query += str(temp) + "')"
    
    print(query)
    
    c = conn.cursor()
    
    c.execute(query)
    
    conn.commit()
    
def ExterneData():
    source = requests.get('https://knmi.nl/nederland-nu/weer/waarnemingen').text
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    Time = datetime.datetime.now().strftime("%H:%M:00")
    soup = BeautifulSoup(source, 'html.parser')   
    lijst = []
    for data in soup.find_all("td"):
        data = data.string
        if data == None:
            data = "none"
        lijst.append(data)
    tempM = lijst[-6]
    luchtvochtigheidM = lijst[-5]
    luchtdrukM = lijst[-1]
    tempV = lijst[-102]
    luchtvochtigheidV = lijst[-101]
    luchtdrukV = lijst[-97]
    
    query = "INSERT INTO ExterneBron (Datum, Tijd, LuchtvochtigheidM, LuchtdrukM, TemperatuurM, LuchtvochtigheidV, LuchtdrukV, TemperatuurV) VALUES ("
    query += "'" + date + "','"
    query += Time + "','"
    query += luchtvochtigheidM + "','"
    query += luchtdrukM + "','"
    query += tempM + "','"
    query += luchtvochtigheidV + "','"
    query += luchtdrukV + "','"
    query += str(tempV) + "')"
    
    print(query)
    
    c = conn.cursor()
    
    c.execute(query)
    
    conn.commit()
    
if __name__ == '__main__':
    try:
        #setup()
        loop()
    except KeyboardInterrupt:
        conn.close()
        pass    
