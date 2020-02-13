"""
USB GPS handler, simple serial reader with parsing
Note: Only one consumer can use this object because serial ports cannot be shared
Sentence: RMC
0 - sentence
1 - UTC of fix
2 - Status A=active, V=void
3 - Latitude
4 - Longitude
5 - Speed (knots)
6 - Track angle in degrees
7 - Date
8 - Magnetic variance
9 - checksum

Author: Howard Webb
Date: 2018/10/04

"""
from __future__ import print_function
import serial
from PortScan import PortScan
from LogUtil import Logger


class GPS(object):
    ''' GPS object '''

#    def __init__(self, callback, port='/dev/ttyUSB0'):
    def __init__(self, callback, port=None, logger=None):
        """
        Get the GPS data and print it with the callback function
        :param callback: The callback function
        :param port: The port for the GPS
        """
        self._callback = callback
        self._logger=logger
        if logger==None:
            self._logger=Logger("GPS", Logger.INFO)
            
        if port == None:
            port = self.findPort()
        self._port = None
        try:
            self._port = serial.Serial(port, baudrate=4800, timeout=1)
        except Exception as e:
            self._logger.error(e)
            
    def findPort(self):
        ps = PortScan(self._logger)
        port_list = ps.getPorts()
        if 'GPS' in port_list.keys():
            return port_list['GPS']
        else:
            return None

    def watch(self):
        """
        infinite loop to watch the GPS. For each new record, parse it and pass it to the callback
        :return:
        """
        while True:
            self.get()

    # noinspection PyUnusedLocal
    def get(self):
        """
        reads the gPS value and prints it with the callback function
        :return: None
        """

        if self._port is None:
            values = {'name': None, 'data': None}
            self._callback(values)
            return

        if self._port.inWaiting() > 0:
            ''' Get sentence without blocking '''
            new_data = self._port.readline().decode('ascii', errors='replace')
            if new_data:
                values = []
                sentence = new_data.split(',')
                self._logger.detail("{} {}".format("Sentence", sentence[0]))
                if sentence[0] == '$GPRMC':
                    for word in sentence:
                        self._logger.detail("{}: {}".format("WORD", word))
                    date = '20' + sentence[9][4:6] + '/' + sentence[9][2:4] + '/' + sentence[9][0:2]
                    time = sentence[1][0:2] + ':' + sentence[1][2:4] + ':' + sentence[1][4:6]
                    timestamp = date + 'T' + time
                    DD = int(float(sentence[3]) / 100)
                    SS = float(sentence[3]) - DD * 100
                    LatDec = DD + SS / 60
                    if sentence[4] == 'S':
                        LatDec = LatDec * -1

                    DD = int(float(sentence[5]) / 100)
                    SS = float(sentence[5]) - DD * 100
                    LonDec = DD + SS / 60
                    if sentence[6] == 'W':
                        LonDec = LonDec * -1

                    #                        print "Time: ", timestamp, LatDec, LonDec
                    values = {'name': sentence[0][1:], 'data': {'time': timestamp, 'lat': LatDec, 'lon': LonDec}}
                    #                        print values
                    self._callback(values)


def testCallback(value):
    ''' callback for test, simply print content '''
    print(value)


def test():
    ''' Test function for GPS object '''
    print("Testing GPS")
    main(Logger.DETAIL)
    
def main(level=Logger.INFO):    
    ''' Test function for GPS object '''
    print("Testing GPS")
    s = GPS(testCallback)
    s._logger.setLevel(level)
    s.watch()


if __name__ == "__main__":
    main()
