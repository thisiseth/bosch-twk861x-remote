from machine import Pin, Signal
import time, board

pin_led_power = Pin(board.PIN_LED_POWER, mode=Pin.IN)
pin_led_70 = Pin(board.PIN_LED_70, mode=Pin.IN)
pin_led_80 = Pin(board.PIN_LED_80, mode=Pin.IN)
pin_led_90 = Pin(board.PIN_LED_90, mode=Pin.IN)
pin_led_100 = Pin(board.PIN_LED_100, mode=Pin.IN)
pin_led_keepwarm = Pin(board.PIN_LED_KEEPWARM, mode=Pin.IN)

signal_led_power = Signal(pin_led_power, invert=False)
signal_led_70 = Signal(pin_led_70, invert=True)
signal_led_80 = Signal(pin_led_80, invert=True)
signal_led_90 = Signal(pin_led_90, invert=True)
signal_led_100 = Signal(pin_led_100, invert=True)
signal_led_keepwarm = Signal(pin_led_keepwarm, invert=True)

pin_button_power = Pin(board.PIN_BUTTON_POWER_RELAY, mode=Pin.OUT, value=0)
pin_button_tempdown = Pin(board.PIN_BUTTON_TEMPDOWN, mode=Pin.OUT, value=0)
pin_button_tempup = Pin(board.PIN_BUTTON_TEMPUP, mode=Pin.OUT, value=0)
pin_button_keepwarm = Pin(board.PIN_BUTTON_KEEPWARM, mode=Pin.OUT, value=0)

pins_button = [pin_button_power, pin_button_tempdown, pin_button_tempup, pin_button_keepwarm]

def leds_json():
    if not signal_led_power():
        return '{"led_power":0,"led_70":0,"led_80":0,"led_90":0,"led_100":0,"led_keepwarm":0}'
    
    return f'{{"led_power":{signal_led_power()},"led_70":{signal_led_70()},"led_80":{signal_led_80()},"led_90":{signal_led_90()},"led_100":{signal_led_100()},"led_keepwarm":{signal_led_keepwarm()}}}'
    
def press_button(button_number):
    button = pins_button[button_number]
    button.value(1)
    time.sleep_ms(250)
    button.value(0)
    time.sleep_ms(50)