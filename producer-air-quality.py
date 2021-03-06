# basic import for the producer
import json
import time
import urllib.request
from kafka import KafkaProducer


#url sample : "https://api.waqi.info/map/bounds/?latlng=X1,Y1,X2,Y2&token=id_token"
url = "https://api.waqi.info/map/bounds/?latlng=49.284348216267716,1.4740693797897653,48.25525522479994,3.280247216173562&token=ce42170db82a8625d285c8b2373c9c916068b1da"

# connecting to the kafka brokers
producer = KafkaProducer(bootstrap_servers=['localhost:9091', 'localhost:9092', 'localhost:9093'])

# while True to have an infinite loop, with a time sleep 5 
while True:

    # call the api
    response = urllib.request.urlopen(url)
    # load the response in a dict()
    stations_temp = json.loads(response.read().decode())

    # we retrieve the sub dictionnary data
    air_stations = stations_temp.get('data')


    for station in air_stations:
        # we log the station
        print(station)
        # then we send it to the brokers
        producer.send("air-station-topic", json.dumps(station).encode())
    print("Produced {} station records".format(len(air_stations)))
    time.sleep(5)