from machine import Pin, Signal
import machine, time

PIN_WEBREPL_SWITCH = 5

PIN_STATUS_LED_R = 15
PIN_STATUS_LED_G = 6
PIN_STATUS_LED_B = 7

PIN_LED_POWER = 41
PIN_LED_70 = 39
PIN_LED_80 = 37
PIN_LED_90 = 36
PIN_LED_100 = 40
PIN_LED_KEEPWARM = 38

PIN_BUTTON_POWER_RELAY = 18
PIN_BUTTON_TEMPDOWN = 9
PIN_BUTTON_TEMPUP = 11
PIN_BUTTON_KEEPWARM = 47

pin_webrepl_switch = Pin(PIN_WEBREPL_SWITCH, mode=Pin.IN, pull=Pin.PULL_DOWN)

signal_use_webrepl = Signal(pin_webrepl_switch, invert=True)

use_webrepl = signal_use_webrepl()

def webrepl_switch_isr(_):
    time.sleep_ms(50)
    
    if use_webrepl == signal_use_webrepl():
        return
    
    import statusLed
    statusLed.blue()
    machine.reset()
    
pin_webrepl_switch.irq(webrepl_switch_isr, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)