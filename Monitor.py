"""
Author: Howard Webb
Date: 10/09/2018

Controller to collect GPS and Sonar data and integrate into a single record
May also collect non-serial data (ie. turbidity)
Store to a file, incrementing for each new run
"""
from __future__ import print_function
from GPS import GPS
from Sonar import Sonar
# from oneWireTemp import getTempC
# from Turbidity import Turbidity
import serial
# Routine to check serial ports for GPS or Sonar messages
# No guarantee which device is on which port
from PortScan import PortScan
from LogUtil import Logger
from Led import Led  # indicators for working sonar and gps

class Monitor(object):
    
    def __init__(self, level=Logger.INFO):
        """
        Build monitor with GPS and Sonar
        :param logger:
        """
        # Normally called logger, but is for debug info
        self._logger = Logger("Monitor", level)
        self._logger.detail("Initialize Monitor")            

        # Object level holders for data
        self._rmc = None
        self._dpt = None
        self._mtw = None
        # Option to use test logger or recording logger
        #        self._tur = Turbidity()
        # Get file for logging data
        self._file_name = self.getFileName()
        self._file = self.openFile()
        self._GPS = None
        self._Sonar = None
        self._led = Led(self._logger)
        # Get list of ports and check who is using
        #  avoids problems when switch USB location
        ps = PortScan(self._logger)
        port_list = ps.getPorts()
        if 'GPS' in port_list.keys():
            self._GPS = GPS(self.recorder, port_list['GPS'], logger=self._logger)
        else:
            # Fail gracefully
            self._GPS = None
            self._logger.error("No GPS port found")
            raise SystemExit
            
        if 'Sonar' in port_list.keys():
            self._Sonar = Sonar(self.recorder, port_list['Sonar'])
        else:
            # Fail 
            self._Sonar = None
            self._logger.error("No Sonar port found")
            raise SystemExit
        self._logger.detail("{}: {}".format("Serial Port Usage", port_list))
        # Start data looping
        while True:
            self._GPS.get()
            self._Sonar.get()
            
    def getFileName(self):
        """
        Create file name for next log
            Assumes format 'Log_000.txt'
            Will incriment the number for the next file
        :return: the filename
        """
        import glob
        filename = '/home/pi/Data/Log_000.txt'
        files = glob.glob("/home/pi/Data/*.txt")
        if len(files) > 0:
            files.sort()
            last_file = files[-1]
            next_nbr = int(last_file.split('.')[0].split('_')[1])
            next_nbr += 1
            filename = "{}{}{}".format('/home/pi/Data/Log_', format(next_nbr, '0>3'), '.txt')
        self._logger.info("{}: {}".format("Logging to", filename))
        return filename

    def openFile(self):
        """
        Open a file for logging data
        :return: the file descriptor
        """
        return open(self._file_name, 'a')

    def save(self, rec):
        """
        appandes the characters in rec into the file
        :param rec: the characters to be saved
        :return: None, but also prints the rec
        """
        self._file.write(rec)
        self._file.flush()
        self._logger.detail(rec)

    def recorder(self, values):
        """
        Callback to get messages, when have all three - save them as one record. A log value is printed
        when all measurement values have non None values.
        :param values:
        :return: None
        """
        #        print "Values", values
        if values['name'] is None:
            self._logger.detail("No Msg Name")
        if values['name'] == 'GPRMC':  # Time and location
            self._logger.detail("GPRMC (time, location) Msg")            
            self._rmc = values['data']
            self._led.On(Led.GPS_LED)
        elif values['name'] == 'SDDBT':  # Depth
            self._logger.detail("SDDBT (depth) Msg")                        
            self._dpt = values['data']
            self._led.On(Led.SONAR_LED)
        elif values['name'] == 'YXMTW':  # Temperature
            self._logger.detail("YXMTW (temp) Msg")                        
            self._mtw = values['data']
        # Save record when have all parts            
        if (self._rmc is not None) and (self._dpt is not None) and (self._mtw is not None):
            self.finishLogging()
            # clear data for next round of sentences
            self._rmc = None
            self._dpt = None
            self._mtw = None
            self._led.Off(Led.GPS_LED)
            self._led.Off(Led.SONAR_LED)

    def finishLogging(self):
        """
        save the logging data to the file
        :return: None
        """
        """ Save data to file """
        # Get non serial data
        #        temp1 = getTempC(0)
        #        temp2 = getTempC(1)
        #        tb = self._tur.getRaw()
        rec = "\n{}, {}, {}, {}, {}".format(self._rmc['time'], self._rmc['lat'], self._rmc['lon'], self._dpt['depth'],
                                          self._mtw["temp"])
        self._logger.debug(rec)
        self.save(rec)


def test():
    """ Quick test with dummy logger """
    print("Test Monitor")
    main(Logger.DEBUG)

def main(level=Logger.INFO):    
    mon = Monitor(level)

if __name__ == "__main__":
        main()
