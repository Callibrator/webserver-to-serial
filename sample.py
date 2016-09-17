import serial2server


ser = serial2server.server('/dev/ttyUSB0',port=80,listen=2)
ser.setTimeout(5)
ser.html_error_file = "/var/www/py2serial/error.html"
ser.setServerDir('/var/www/py2serial/')
ser.contentLength(True)
ser.setWait(0.5)
ser.parseArgs(True)
#ser.setMode('raw')
ser.set404('/var/www/py2serial/404.html')
ser.icon_types.append('jpeg')
ser.startServer()
