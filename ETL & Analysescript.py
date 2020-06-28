import sqlite3
import os
import os.path

def create_connection():
    try:
        conn = sqlite3.connect("C://Users//Gebruiker//Documents//iipbdama//databases//rauweWeerstation.db")
    except Error as e:
        print(e)

    return conn

def create_cursor(conn):
    cursor = conn.cursor()
    
    return cursor

def deleteUrenBuitenAnalyse(conn, cursor):
    # Deleting single record now
    m = 0
    mm = 0
    h = 0
    hh = 0
    query = ''
    for i in range((60 * 14)-1):
        m += 1
        if m == 10:
            m = 0
            mm += 1
        if mm == 6:
            mm = 0
            h += 1
        if h == 10:
            h = 0
            hh += 1
        if (str(hh)+str(h)+":"+str(mm)+ str(m)) == "10:00":
            m = 1
            mm = 0
            h = 0
            hh = 2
        if (str(hh)+str(h)+":"+str(mm)+ str(m)) == "24:00":
            m = 0
            mm = 0
            h = 0
            hh = 0

        query = "DELETE from ExterneBron where Tijd = '" + str(hh) + str(h) + ":" + str(mm) + str(m) + ":00'; "
        cursor.execute(query)
        print(query)
        query = "DELETE from Temperatuur where Tijd = '" + str(hh) + str(h) + ":" + str(mm) + str(m) + ":00'; "
        cursor.execute(query)
        print(query)
        query = "DELETE from Luchtvochtigheid where Tijd = '" + str(hh) + str(h) + ":" + str(mm) + str(m) + ":00'; "
        cursor.execute(query)
        print(query)
        conn.commit()
        
def deleteDagenBuitenAnalyse(conn, cursor):
    query = "DELETE from ExterneBron where Datum = '2020-06-10'; "
    cursor.execute(query)
    print(query)
    query = "DELETE from Temperatuur where Datum = '2020-06-10'; "
    cursor.execute(query)
    print(query)
    conn.commit()

def creeerVerDagenTabel(path, bestand, naam):
    dagen = 11
    lines = ''
    for dag in range(10):
        with open(path+ naam+ str(dagen) +".csv", 'w') as wfile:
            with open(path + bestand, "r") as rfile:
                 for line in rfile:
                        if ('2020-06-'+str(dagen)) in line:
                            wfile.write(line)
                            print(line)
        dagen += 1

def puntenOmzetten(path, bestand, naam):
    lines = ''
    with open(path+"commacorrected" + naam +".csv", 'w') as wfile:
        with open(path + bestand, "r") as rfile:
             for line in rfile:
                    line = line.replace("." , ",")
                    wfile.write(line)
                    print(line)

def gemTempDrukVochtPerDag(conn, cursor):
    query = "CREATE TABLE Averages (Datum DATE PRIMARY KEY, GemTempSen NUMERIC, GemTempM NUMERIC, GemTempV NUMERIC, GemVochtSen INTEGER, GemVochtM INTEGER, GemVochtV INTEGER, GemDrukSen NUMERIC, GemDrukM NUMERIC, GemDrukV NUMERIC);"
    cursor.execute(query)
    conn.commit()
    print(query)
###################################### temperatuur 
    query = "SELECT Datum, AVG(TemperatuurM) FROM ExterneBron GROUP BY Datum; "
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    datumL = []
    GemTempML = []
    for row in rows:
        datum = row[0]
        temp = "%.2f" % row[1]
        GemTempM = str(temp)
        datumL.append(datum)
        GemTempML.append(GemTempM)
        print("De gemiddelde temperatuur in Maastricht op de dag: " + datum + " was " + temp + " °C")
    print(datumL)

    query = "SELECT Datum, AVG(TemperatuurV) FROM ExterneBron GROUP BY Datum; "
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    GemTempVL = []
    for row in rows:
        datum = row[0]
        temp = "%.2f" % row[1]
        GemTempV = str(temp)
        GemTempVL.append(GemTempV)
        print("De gemiddelde temperatuur in Voorschoten op de dag: " + datum + " was " + temp + " °C")


    query = "SELECT Datum, AVG(temperature) FROM Temperatuur GROUP BY Datum; "
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    GemTempSenL = []
    for row in rows:
        datum = row[0]
        temp = "%.2f" % row[1]
        GemTempSen = str(temp)
        GemTempSenL.append(GemTempSen)
        print("De gemiddelde temperatuur van de sensor op de dag: " + datum + " was " + temp + " °C")
########################### luchtvochtigheid
    query = "SELECT Datum, AVG(LuchtvochtigheidM) FROM ExterneBron GROUP BY Datum; "
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    GemVochtML = []
    for row in rows:
        datum = row[0]
        Vocht = "%.2f" % row[1]
        GemVochtM = str(Vocht)
        GemVochtML.append(GemVochtM)
        print("De gemiddelde Luchtvochtigheid in Maastricht op de dag: " + datum + " was " + Vocht + " %")

    query = "SELECT Datum, AVG(LuchtvochtigheidV) FROM ExterneBron GROUP BY Datum; "
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    GemVochtVL = []
    for row in rows:
        datum = row[0]
        Vocht = "%.2f" % row[1]
        GemVochtV = str(Vocht)
        GemVochtVL.append(GemVochtV)
        print("De gemiddelde Luchtvochtigheid in Maastricht op de dag: " + datum + " was " + Vocht + " %")

    query = "SELECT Datum, AVG(Humiture) FROM Luchtvochtigheid GROUP BY Datum; "
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    GemVochtSenL = []
    for row in rows:
        datum = row[0]
        Vocht = "%.2f" % row[1]
        GemVochtSen = str(Vocht)
        GemVochtSenL.append(GemVochtSen)
        print("De gemiddelde Luchtvochtigheid van de sensor op de dag: " + datum + " was " + Vocht + " %")
############################### luchtdruk
    query = "SELECT Datum, AVG(luchtdrukM) FROM ExterneBron GROUP BY Datum; "
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    GemDrukML = []
    for row in rows:
        datum = row[0]
        druk = "%.2f" % row[1]
        GemDrukM = str(druk)
        GemDrukML.append(GemDrukM)
        print("De gemiddelde luchtdruk in Maastricht op de dag: " + datum + " was " + druk + " hPa")

    query = "SELECT Datum, AVG(luchtdrukV) FROM ExterneBron GROUP BY Datum; "
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    GemDrukVL = []
    for row in rows:
        datum = row[0]
        druk = "%.2f" % row[1]
        GemDrukV = str(druk)
        GemDrukVL.append(GemDrukV)
        print("De gemiddelde luchtdruk in Maastricht op de dag: " + datum + " was " + druk + " hPa")

    """query = "SELECT Datum, AVG(temperature) FROM Temperatuur GROUP BY Datum; "
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    GemTempSenL = []
    for row in rows:
        datum = row[0]
        temp = "%.2f" % row[1]
        GemTempSen = str(temp)
        GemTempSenL.append(GemTempSen)
        print("De gemiddelde temperatuur van de sensor op de dag: " + datum + " was " + temp + " hPa")"""
    i = 0
    a = 0
    for keren in range(10):
        if str(datum[i]) == "2020-06-19" or "2020-06-20" or "2020-06-21" or "2020-06-22" or "2020-06-23":
            GemTempSenL.append("NULL")
        if str(datum[i]) == "2020-06-21" or "2020-06-22" or "2020-06-23":
            GemVochtSenL.append("NULL")
        if i == 5:
            query = "INSERT INTO Averages VALUES ("+str(datumL[i])+","+GemTempSenL[i]+","+GemTempML[i]+","+GemTempVL[i]+",NULL,"+GemVochtML[i]+","+GemVochtVL[i]+",NULL,"+GemDrukML[i]+","+GemDrukVL[i]+");"
            print(query)
            cursor.execute(query)
            conn.commit()
            i += 1
            a -= 1
            continue
        
        query = "INSERT INTO Averages VALUES ("+str(datumL[i])+","+GemTempSenL[i]+","+GemTempML[i]+","+GemTempVL[i]+","+GemVochtSenL[i+a]+","+GemVochtML[i]+","+GemVochtVL[i]+",NULL,"+GemDrukML[i]+","+GemDrukVL[i]+");"
        print(query)
        cursor.execute(query)
        conn.commit()
        i += 1

def gemiddeldenDataset(conn, cursor):
    query = "SELECT AVG(GemTempSen), AVG(GemTempV), AVG(GemTempM) FROM Averages; "
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    for row in rows:
        print("Gemiddelde temperatuur van de sensor: "+ str("%.2f" % row[0]))
        print("Gemiddelde temperatuur in Voorschoten: "+ str("%.2f" % row[1]))
        print("Gemiddelde temperatuur in Maastricht: "+ str("%.2f" % row[2]))
        
    query = "SELECT AVG(GemVochtSen), AVG(GemVochtV), AVG(GemVochtM) FROM Averages; "
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    for row in rows:
        print("Gemiddelde luchtvochtigheid van de sensor: " """ str("%.2f" % row[0])""")
        print("Gemiddelde luchtvochtigheid in Voorschoten: "+ str("%.2f" % row[1]))
        print("Gemiddelde luchtvochtigheid in Maastricht: "+ str("%.2f" % row[2]))
    
    query = "SELECT AVG(GemDrukSen), AVG(GemDrukV), AVG(GemDrukM) FROM Averages; "
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    for row in rows:
        print("Gemiddelde luchtdruk van de sensor: " """str("%.2f" % row[0])""")
        print("Gemiddelde luchtdruk in Voorschoten: "+ str("%.2f" % row[1]))
        print("Gemiddelde luchtdruk in Maastricht: "+ str("%.2f" % row[2]))
    
def main():
    conn = create_connection()
    cursor = create_cursor(conn)

    #  Onnodige data uit de tabellen halen
    #####
    #deleteDagenBuitenAnalyse(conn, cursor)
    #deleteUrenBuitenAnalyse(conn, cursor)
    #####
    
    # Exporteer nu de file naar csv om power BI grafieken te maken voor aparte dagen
    #####
    #puntenOmzetten("C://Users//Gebruiker//Documents//iipbdama//databases//", "Temperatuur.csv", "Temperatuur")
    #creeerVerDagenTabel("C://Users//Gebruiker//Documents//iipbdama//databases//", "Luchtvochtigheid.csv", "Luchtvochtigheid")
    #####

    # Analyse Queries
    #####
    gemTempDrukVochtPerDag(conn, cursor)
    #gemiddeldenDataset(conn, cursor)
    #####
if __name__ == "__main__":
    main()
