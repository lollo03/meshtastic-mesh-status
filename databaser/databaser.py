import paho.mqtt.client as mqtt
import json
import re
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()



mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)



def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("msh/2/stat/updates")

def on_message(client, userdata, msg):
    x = json.loads(msg.payload)
    reporter = x['reporter'].split()[0]
    originale = re.split('.(!........)', x['message'])[1]
    
    
    print("Avvistato nodo " + originale)
    sql = "INSERT INTO `devices` (`node_id`, `last_seen`, `via`) VALUES ('{reporter}', NOW(), '{reporter}') ON DUPLICATE KEY UPDATE last_seen = NOW();".format(reporter= reporter)
    cursore.execute(sql)
    mydb.commit()

    
    if(originale != reporter):
        sql = "INSERT INTO `devices` (`node_id`, `last_seen`, `via`) VALUES ('{originale}', NOW(), '{reporter}') ON DUPLICATE KEY UPDATE last_seen = NOW();".format(originale= originale, reporter= reporter)
        cursore.execute(sql)
        mydb.commit()


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASSWORD"))

mqttc.connect(os.getenv("MQTT_HOST"), 1883, 60)

cursore = mydb.cursor()



# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()