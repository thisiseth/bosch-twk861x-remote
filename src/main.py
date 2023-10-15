from machine import Pin
import network, kettleConfig

print('main.py')

try:
    import statusLed
    statusLed.yellow()
except:
    pass

network.hostname(kettleConfig.WIFI_HOSTNAME)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print('attempting wlan')

if not wlan.isconnected():
    wlan.connect(kettleConfig.WIFI_SSID, kettleConfig.WIFI_PASSWORD)

    while not wlan.isconnected():
        pass

print('network config:', wlan.ifconfig())

import board

if board.use_webrepl:
    statusLed.red()
else:
    statusLed.off()

import webMain

webMain.init()
