#!/usr/bin/env python

import time
import board
import adafruit_dht
from prometheus_client import start_http_server, Gauge

TEMPERATURE_GAUGE = Gauge('dht_temperature_celsius', 'Current temperature read from DHT sensor.')
HUMIDITY_GAUGE = Gauge('dht_humidity_percent', "Current humidity read from DHT sensor.")

READ_FAILS = 0

READ_FAIL_THRESHOLD = 60


# Initialize the DHT device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)

def read_from_sensor():
    global READ_FAILS

    try:
        print('Reading from sensor...')
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity

        print(
            'Got values: (temperature, humidity, count of read fails)',
            temperature, humidity, READ_FAILS)

        TEMPERATURE_GAUGE.set(temperature)
        HUMIDITY_GAUGE.set(humidity)
        READ_FAILS = 0
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        READ_FAILS += 1
        print('Failed to read data:', READ_FAILS, error.args[0])

    if READ_FAILS > READ_FAIL_THRESHOLD:
        TEMPERATURE_GAUGE.set(-1)
        HUMIDITY_GAUGE.set(-1)


if __name__ == "__main__":
    print("Starting Prometheus Temperature Client")
    start_http_server(9842)
    TEMPERATURE_GAUGE.set(-1)
    HUMIDITY_GAUGE.set(-1)
    print("Server successfully started. Reading temperature every 5 seconds.")
    read_from_sensor()

    while True:
        try:
            time.sleep(5)
            read_from_sensor()
        except Exception as exception:
            print("Failed to read data from sensor", type(exception), exception)