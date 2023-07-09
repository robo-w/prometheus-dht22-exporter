# Prometheus DHT22 Exporter

Python script to read temperature and humidity data from a DHT22 sensor
and expose the data via Prometheus interface.

## Versions

* `v1`: Uses the outdated `Adafruit_DHT` library.
* `v2`: Updated version to use the `adafruit_dht` library.

## Preconditions

`sudo pip3 install prometheus-client adafruit-circuitpython-dht RPi.GPIO==0.7.1a4`
