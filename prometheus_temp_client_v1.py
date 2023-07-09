#!/usr/bin/env python

import time

import Adafruit_DHT
from prometheus_client import start_http_server, Gauge

TEMPERATURE_GAUGE = Gauge('dht_temperature_celsius', 'Current temperature read from DHT sensor.')
HUMIDITY_GAUGE = Gauge('dht_humidity_percent', "Current humidity read from DHT sensor.")

READ_FAILS_TEMPERATURE = 0
READ_FAILS_HUMIDITY = 0

READ_FAIL_THRESHOLD = 30


def read_from_sensor():
    global READ_FAILS_TEMPERATURE, READ_FAILS_HUMIDITY

    print('Reading current temperature from sensor...')
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
    print(
        'Got values: (temperature, humidity, temperature read fails, humidity read fails)',
        temperature, humidity,
        READ_FAILS_TEMPERATURE, READ_FAILS_HUMIDITY)

    if temperature is not None:
        TEMPERATURE_GAUGE.set(temperature)
        READ_FAILS_TEMPERATURE = 0
    else:
        READ_FAILS_TEMPERATURE += 1

    if humidity is not None:
        HUMIDITY_GAUGE.set(humidity)
        READ_FAILS_HUMIDITY = 0
    else:
        READ_FAILS_HUMIDITY += 1

    if READ_FAILS_TEMPERATURE > READ_FAIL_THRESHOLD:
        TEMPERATURE_GAUGE.set(-1)

    if READ_FAILS_HUMIDITY > READ_FAIL_THRESHOLD:
        HUMIDITY_GAUGE.set(-1)


if __name__ == "__main__":
    print("Starting Prometheus Temperature Client")
    start_http_server(9842)
    TEMPERATURE_GAUGE.set(-1)
    HUMIDITY_GAUGE.set(-1)
    print("Server successfully started. Reading temperature every 20 seconds.")

    while True:
        read_from_sensor()
        time.sleep(20)
