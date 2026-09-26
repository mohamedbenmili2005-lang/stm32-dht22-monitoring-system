from flask import Flask, jsonify, render_template
import cx_Oracle
app = Flask(__name__)

dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")
conn = cx_Oracle.connect("SYSTEM", "mmm555++", dsn)
cur= conn.cursor()
cure= conn.cursor()
@app.route("/dzata", methods=["GET"])
def get_data():
    
  
    cur.execute("""
        SELECT temp, hum, dates
        FROM pro.capteur c 
    """)
   
    rows = cur.fetchall()

    dzata = []
    for row in rows:
        dzata.append({
            "temp": row[0],
            "hum": row[1],
            "dates":row[2],

        })
   
    return jsonify(dzata)
@app.route("/")
def index():
    return render_template("index.html")
app.run(host="0.0.0.0", port=5000)
