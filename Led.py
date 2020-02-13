'''
Class for indicator leds


'''

import RPi.GPIO as GPIO
from LogUtil import Logger
from time import sleep

class Led(object):

    GPS_LED = 13
    SONAR_LED = 15

    def __init__(self, logger=None, level=Logger.INFO):
        """
        Setup for indicator leds
        :param logger:
        """
        # Normally called logger, but is for debug info
        self._logger = logger
        if logger == None:
            self._logger = Logger("Led", level)
        self._logger.debug("Initialize Leds")
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        
        # Create a dictionary called pins to store the pin number, name, and pin state:
        self._pins = {
           Led.GPS_LED : {'name' : 'GPS_LED', 'state' : GPIO.LOW},
           Led.SONAR_LED : {'name' : 'SONAR_LED', 'state' : GPIO.LOW}
        }           
        

        # Set each pin as an output and make it low:
        for pin in self._pins:
           self._logger.debug("{}: {}".format("Initialize Pin", pin)) 
           GPIO.setup(pin, GPIO.OUT)
           self.Off(pin)
           
    def Off(self, pin):
      GPIO.output(pin, GPIO.LOW)
      self._logger.debug("{} {}".format(pin, "Off"))      
        
    def On(self, pin):
      GPIO.output(pin, GPIO.HIGH)
      self._logger.debug("{} {}".format(pin, "On"))
      
def test():
    print("Testing LEDs")
    print("Create Led")
    led = Led(level=Logger.DEBUG)
    print("Set Debug on")
    print("Start")
    for x in range(0, 5):
        print("On")
        #led.On(Led.GPS_LED)
        led.On(Led.SONAR_LED)
        led.On(Led.GPS_LED)        
        sleep(3)
        print("Off")
        #led.Off(Led.GPS_LED)
        led.Off(Led.SONAR_LED)
        led.Off(Led.GPS_LED)        
        sleep(3)
        
if __name__ == "__main__":
        test()        
        
        

        

        


    