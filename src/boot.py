# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)

use_webrepl = True

try:
    import board, machine
    use_webrepl = board.use_webrepl
    
    if machine.reset_cause() == machine.SOFT_RESET:
        import statusLed
        statusLed.green()
except:
    pass

if use_webrepl:
    import webrepl
    webrepl.start()
