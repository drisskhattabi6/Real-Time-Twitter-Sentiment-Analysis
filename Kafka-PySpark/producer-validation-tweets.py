from time import sleep
import csv 
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         json.dumps(x).encode('utf-8'))

with open('twitter_validation.csv') as file_obj:
    reader_obj = csv.reader(file_obj)
    for data in reader_obj: 
        # print(data)
        producer.send('numtest', value=data)
        sleep(3)