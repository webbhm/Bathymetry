"""
Code modified from:
apps.fishandwhistle.net/archives/1155

"""
from __future__ import print_function
import serial
import sys
import glob
from LogUtil import Logger

class PortScan(object):

    def __init__(self, logger=None):
        """
        Build monitor with GPS and Sonar
        :param logger:
        """
        # Normally called logger, but is for debug info
        self._portList = {}
        self._logger = logger
        if self._logger == None:
            self._logger = Logger("Monitor", Logger.INFO)
        self._logger.debug("Initialize Monitor")

    def identifyPort(self, port):
        """
        tests the port and identifies what device is attached to it from probing it
        :param port:
        :return: a port list dict with the tho porst for 'GPS' and 'Sonar'
        """
        try:
            with serial.Serial(port, baudrate=4800, timeout=1) as ser:
                # read 10 lines from the serial output
                for i in range(10):
                    line = ser.readline().decode('ascii', errors='replace')
                    msg = line.split(',')
                    if msg[0] == '$GPRMC':
                        self._portList['GPS'] = port
                        return
                    elif msg[0] == '$SDDBT':
                        self._portList['Sonar'] = port
                        return

        except Exception as e:
            self._logger.error(e)


    def scanPorts(self):
        """
        scan the ports on various devices including Windows, linux, and OSX
        :return:
        """
        if sys.platform.startswith('win'):
            self._logger.debug("scan Windows")
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            self._logger.debug("scan Linux")
            # this excludes your current terminal "/dev/tty"
            patterns = ('/dev/tty[A-Za-z]*', '/dev/ttyUSB*')
            ports = [glob.glob(pattern) for pattern in patterns]
            ports = [item for sublist in ports for item in sublist]  # flatten
        elif sys.platform.startswith('darwin'):
            self._logger.debug("scan Darwin")
            patterns = ('/dev/*serial*', '/dev/ttyUSB*', '/dev/ttyS*')
            ports = [glob.glob(pattern) for pattern in patterns]
            ports = [item for sublist in ports for item in sublist]  # flatten
        else:
            self._logger.error("Unsupported Platform")
            raise EnvironmentError('Unsupported platform')
        for port in ports:
            self._logger.debug(port)
        return ports


    def getPorts(self):
        """
        get the ports
        :return: return the ports dict
        """
        ports = self.scanPorts()
        for port in ports:
            self.identifyPort(port)
        for port in self._portList:
            self._logger.info("{} on {}".format(port, self._portList[port]))
        return self._portList


def test():
    print("Test Port Scan")
    ps = PortScan()
    ps._logger.setLevel(Logger.DETAIL)
    list = ps.getPorts()

if __name__ == "__main__":
    test()
