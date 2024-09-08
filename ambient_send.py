# SoratobuMacaroniPenguin
# for Micropython-1.23.0 later
# upload iot server https://ambient.
# used library
#     ambient github
#     max31865 bithub

import time
import machine as board
from machine import Pin , SoftSPI
import max31865 as adafruit_max31865 
MISO = 14
MOSI = 5
SCK = 4
CS = 0

import ambient
import urequests as requests
CHANNEL_ID = '--channel id--'
WRITE_KEY = '--write key--'

import urequests

import network
SSID = '--ssid--'
KEY = '--key--'

spi = SoftSPI(baudrate=200000, polarity=1, phase=0, sck=Pin(SCK), mosi=Pin(MOSI), miso=Pin(MISO))
cs = CS
sensor = adafruit_max31865.Max31865(spi, cs , rtd_nominal=100, ref_resistor=430.0, wires=3,misoPin=MISO,mosiPin=MOSI,sckPin=SCK)
    

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect( SSID , KEY )
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def max31865_measurement():
    temp = sensor.temperature
    print("Temperature: {0:0.3f}C".format(temp))
    return temp


def main():
    do_connect()
    am = ambient.Ambient( CHANNEL_ID , WRITE_KEY)

    while True:
        temp =max31865_measurement()
        r = am.send({'d1': "{:.1f}".format(temp)})
        print(r.status_code)
        r.close()
        time.sleep(30)


if __name__ == "__main__":
    main()
