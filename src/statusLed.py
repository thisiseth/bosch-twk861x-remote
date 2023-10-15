from machine import Pin, PWM
import board

pin_R = Pin(board.PIN_STATUS_LED_R, mode=Pin.OUT, value=1)
pin_G = Pin(board.PIN_STATUS_LED_G, mode=Pin.OUT, value=1)
pin_B = Pin(board.PIN_STATUS_LED_B, mode=Pin.OUT, value=1)

pwm_R = None
pwm_G = None
pwm_B = None

def color(r, g, b):
    global pwm_R, pwm_G, pwm_B
    
    if r == 0:
        if pwm_R != None:
            pwm_R.deinit()
            pwm_R = None
        pin_R(1)
    else:
        pwm_R = PWM(pin_R, freq=20000, duty=1023-r)
        
    if g == 0:
        if pwm_G != None:
            pwm_G.deinit()
            pwm_G = None
        pin_G(1)
    else:
        pwm_G = PWM(pin_G, freq=20000, duty=1023-g)
        
    if b == 0:
        if pwm_B != None:
            pwm_B.deinit()
            pwm_B = None
        pin_B(1)
    else:
        pwm_B = PWM(pin_B, freq=20000, duty=1023-b)

def red():
    color(1023, 0, 0)

def green():
    color(0, 1023, 0)
    
def blue():
    color(0, 0, 1023)
    
def yellow():
    color(1023, 400, 0)
    
def off():
    color(0, 0, 0)