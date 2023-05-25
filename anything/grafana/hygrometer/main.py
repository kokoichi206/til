import datetime
import time

import dht11
import influxdb
import RPi.GPIO as GPIO

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin=17)


db = influxdb.InfluxDBClient(host="localhost", port=8086, database="sensortag")


def write_to_influxdb(data):
    points = [
        {"measurement": "sensortag", "time": datetime.datetime.utcnow(), "fields": data}
    ]
    db.write_points(points)


while True:
    result = instance.read()
    if result.is_valid():
        data = {}
        data["temperature"] = result.temperature
        data["humidity"] = result.humidity
        write_to_influxdb(data)
    else:
        print("Error: %d" % result.error_code)
    time.sleep(60)
