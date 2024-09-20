# SoratobuMacaroniPenguin
# for Micropython-1.23.0 later
# upload iot server https://ambient.
# used library
#     ambient github
#     max31865 bithub

#base init area
import password_file
import time
import machine
import ntptime
import utime

#sensor init area
from machine import Pin , SoftSPI
import max31865 as adafruit_max31865 
MISO = 14
MOSI = 5
SCK = 4
CS = 0
spi = SoftSPI(baudrate=200000, polarity=1, phase=0, sck=Pin(SCK), mosi=Pin(MOSI), miso=Pin(MISO))
cs = CS
sensor = adafruit_max31865.Max31865(spi, cs , rtd_nominal=100, ref_resistor=430.0, wires=3,misoPin=MISO,mosiPin=MOSI,sckPin=SCK)
max_board_switch = Pin(12 , Pin.OUT)

#ambient send init area
import json
import urequests
#from urequests.exceptions import Timeout
CHANNEL_ID = password_file.CHANNEL_ID
WRITE_KEY = password_file.WRITE_KEY
url = "http://ambidata.io/api/v2/channels/" + CHANNEL_ID +"/data"

#network init area
import network
SSID = password_file.SSID
KEY = password_file.KEY
sta_if = network.WLAN(network.STA_IF)

def do_connect():
    sta_if.active(True)
    sta_if.connect( SSID , KEY )
    while True: 
        print('connecting to network...')
        if sta_if.isconnected():
            print('network config:', sta_if.ifconfig())
            break
        else:
            print('not connected')
            time.sleep(3)

def main():
    do_connect()
    rtc = machine.RTC()
    #rtc.datetime((2017, 8, 23, 1, 12, 48, 0, 0))
    #rtc.datetime()
    ntptime.settime()
    #utime.localtime(utime.mktime(utime.localtime()) + 9 *3600)
    print("UTC=",rtc.datetime())
    while True:
        #wake
        print("wake")
        do_connect()
        max_board_switch.value(1) #max boead on
        time.sleep(0.1)
        temp = sensor.temperature
        d1 = '{:.1f}'.format(temp)
        print("temp",d1)
    
        #send Ambient
        n = utime.localtime(utime.time() + 9 * 3600)
        data = {'created': str(n[0]) + '-' + str(n[1]) + '-' + str(n[2]) + ' ' + str(n[3]) + ':' + str(n[4]) + ':' + str(n[5]), 'writeKey': WRITE_KEY, 'd1' : d1}
        print(data)
        json_data = json.dumps(data)
        print("ambient send")
        try:
            r =urequests.post(url,data=json_data,headers={"Content-Type": "application/json"},timeout=10)
            print("ambient result = ",r.status_code)
        except Timeout:
            print("ambient timeout")
        except urequests.exceptions.RequestException as e:
            print('request failed: ', e)
        
        #sleep準備
        max_board_switch.value(0) #max board off
        sta_if.disconnect()
        sta_if.active(False) #wifi off
        time.sleep(0.1)
        # ライトスリープに入る
        print("go sleep")
        machine.lightsleep(60000)
        

if __name__ == "__main__":
    main()
