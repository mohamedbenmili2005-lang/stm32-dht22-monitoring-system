from PyQt5.QtWidgets import *
from PyQt5.uic import *
import cx_Oracle
import serial
import time


def démarrer_lecture():
    ser = serial.Serial('COM6', 115200, timeout=1)

    print("Réception en temps réel...\n")
    dsn = cx_Oracle.makedsn(
    "localhost",   # ou 7amaBdan
    1521,
    service_name="XE"
    )

    conn = cx_Oracle.connect(
    user="SYSTEM",
    password="mmm555++",
    dsn=dsn
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM pro.capteur")
    print(cur.fetchone())
# Si le propriétaire est 'MONUSER', écrivez :
    sql = "INSERT INTO PRO.capteur (temp,hum) VALUES (:1, :2)"
    while True:
        try:
            ligne = ser.readline().decode().strip()
            if ligne:
                if "TEMP" in ligne:
                    data = ligne.split(";")
                    temp = data[0].split(":")[1]
                    hum = data[1].split(":")[1]
                    print(f"Température : {temp} °C | Humidité : {hum} %")
                    cur.execute(sql, (temp,hum))
                    conn.commit()
                    print("Succès !")
                    curk= conn.cursor()
                    curk.execute("SELECT * FROM pro.capteur")
                    res=curk.fetchall()
                    w.a.setRowCount(0)
                    for i,v in enumerate(res):
                        w.a.insertRow(i)
                        w.a.setItem(i,0,QTableWidgetItem(str(v)))
                else:
                    print(ligne)
    
        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            print(f"Code d'erreur : {error_obj.code}")
            print(f"Message d'erreur : {error_obj.message}")
# Fermeture
        curk= conn.cursor()
        curk.execute("SELECT * FROM pro.capteur")
        res=curk.fetchall()
        w.a.setRowCount(0)
        for i,v in enumerate(res):
            w.a.insertRow(i)
            w.a.setItem(i,0,QTableWidgetItem(str(v)))
        
            


app=QApplication([])
w=loadUi("interface.ui")
w.d.clicked.connect(démarrer_lecture)
w.show()
app.exec_()