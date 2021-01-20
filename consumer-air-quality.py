# basic import for the consumer
from kafka import KafkaConsumer
import json

# connect to the brokers
consumer = KafkaConsumer('air-station-topic', bootstrap_servers=['localhost:9091','localhost:9092','localhost:9093'])
for message in consumer:

    # load the messages received and treat them
    station = json.loads(message.value.decode())
    AQI = station['aqi']
    place = station.get('station')
    ville = place['name']

    # if the AQI is above a certain treshold, the consumer warns the user with a log
    if(AQI != '-'):
        if(int(AQI)> 50):
            print("DANGER : " +ville + " - AQI : "+AQI)
