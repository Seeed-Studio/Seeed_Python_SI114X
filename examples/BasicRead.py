from seeed_si114x import grove_si114x
from seeed_si115x import grove_si115x
import time
import signal
def handler(signalnum, handler):
    print("Please use Ctrl C to quit")
def main():
    try:
        sunlight = grove_si115x()
    except Exception as e:
        try:
            sunlight = grove_si114x()
        except Exception as e:
            print("SunlightSensor.setup: " + str(e))
    print("Please use Ctrl C to quit")
    signal.signal(signal.SIGTSTP, handler) # Ctrl-z
    signal.signal(signal.SIGQUIT, handler) # Ctrl-\
    while True:
        print('Visible %03d UV %.2f IR %03d' % (sunlight.ReadVisible , sunlight.ReadUV/100 , sunlight.ReadIR),end=" ")
        print('\r', end='')
        time.sleep(0.5)
if __name__  == '__main__':
    main()