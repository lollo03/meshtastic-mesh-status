import threading 
import mysql.connector
import requests
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
chat_id = os.getenv("CHAT_ID")

INTERVALLO_ALLERTA = 30



mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)

cursore = mydb.cursor()

gia_allertati = []


def manda_messaggio_offline(nodename):
    nodename = nodename.split("!")[1]
    messaggio =f"Attenzione! {nodename} non si fa vivo da {INTERVALLO_ALLERTA} minuti!"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={messaggio}"
    requests.get(url)
    

def manda_messaggio_online(nodename):
    nodename = nodename.split("!")[1]
    messaggio =f"Buone notizie! {nodename} è tornato online"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={messaggio}"
    requests.get(url)

def loop():
    threading.Timer(10.0, loop).start()
    sql = "SELECT * FROM `devices` WHERE `last_seen` < NOW() - interval " + str(INTERVALLO_ALLERTA) + " MINUTE AND node_id = via"
    cursore.execute(sql)
    myresult = []
    myresult = cursore.fetchall()
    mydb.commit()

    offline = []
    for x in myresult:
        if(x[2] not in gia_allertati ):
            print(f"{x[2]} è offline... mando un messaggio")
            manda_messaggio_offline(x[2])
            gia_allertati.append(x[2])
        else:
            print(f"{x[2]} è già stato segnalato")
        
        if(x[2] not in offline):
            offline.append(x[2])
            


    # rimuovo da gia_allertati nodi che sono tornati online...            
    for x in gia_allertati:
        if x not in offline:
            gia_allertati.remove(x)
            print(f'{x} è tornato online!')
            manda_messaggio_online(x)
    

loop()

