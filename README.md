# Bathymetry
Python code for bathymetry data collection (GPS and sonar)

The purpose of this code is to manage a USB GPS and a USB Sonar unit (AIRMAT DT80), collecting time, temperature, latitude and longitude and saving these as a record to a file.
Monitor.py is the main module that coordinates the other objects.  When the Raspberry Pi starts, it calls this Class.  On initialization it checks the serial ports (USB) for presence of the sensors.  If the sensors are found the program goes into a loop collecting data (which the sensors should push about once a second).  When two records are found, they are combined into a data record and pushed to the file (CSV format).
There is no reporting of the program, so two LEDs are attached to the Raspberry which blink each time the GPS or Sonar produce a record.
