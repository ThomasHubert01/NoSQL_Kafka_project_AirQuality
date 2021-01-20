from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('air-station-topic', bootstrap_servers=['localhost:9091','localhost:9092','localhost:9093'])
for message in consumer:
    station = json.loads(message.value.decode())
    AQI = station['aqi']
    place = station.get('station')
    ville = place['name']
    if(AQI != '-'):
        if(int(AQI)> 50):
            print("DANGER : " +ville + " - AQI : "+AQI)
