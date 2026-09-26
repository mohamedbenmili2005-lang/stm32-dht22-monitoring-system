from PyQt5.QtWidgets import *
from PyQt5.uic import *
import cx_Oracle
from PyQt5.QtCore import QTimer
dsn = cx_Oracle.makedsn(
    "localhost",   
    1521,
    service_name="XE"
)

conn = cx_Oracle.connect(
    user="SYSTEM",
    password="mmm555++",
    dsn=dsn
)


def sensor():
    cur = conn.cursor()
    cur.execute("SELECT * FROM pro.capteur")
    res=cur.fetchall()
    # Si le propriétaire est 'MONUSER', écrivez :
    sql = "INSERT INTO PRO.TEMP (temp,hum,limite,etat) VALUES (:1, :2, :3, :4)"
    w.a.setRowCount(0)
    for i,v in enumerate(res):
        if res:
            temps=v[0]
            w.temp.display(temps)
            hums=v[1]
            w.h.display(hums)
            
        w.a.scrollToBottom()
        w.a.insertRow(i)
        w.a.setItem(i,0,QTableWidgetItem(str(v[0])))
        w.a.setItem(i,1,QTableWidgetItem(str(v[1])))
        w.a.setItem(i,2,QTableWidgetItem(str(v[2])))
        var=w.limite.text()
        if (v[0]>int(var)):
            etat="alert"
            w.a.setItem(i,3,QTableWidgetItem("Alert"))
            QMessageBox.warning(w, "Alert","Attention")
            
        else:
            etat="stable"
            w.a.setItem(i,3,QTableWidgetItem("Stable"))
        cur.execute(sql,(temps,hums,int(var),etat))
        conn.commit()
def démarrer_lecture():
    v=w.refresh.text()
    timer.start(int(v)*1000)


def arreter():
    timer.stop()


app=QApplication([])
w=loadUi("interface.ui")
w.d.clicked.connect(démarrer_lecture)
w.show()
timer = QTimer()
timer.timeout.connect(sensor)
app.exec_()
