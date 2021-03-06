"""
This is a simple class created by Callibrator in order to control serial data and send directly to browser

the server class is responsible for comunication between the browser and the serial port.
methods:
-- Initialize method, Example:
	s = serial2server.server(<required device>,<optional ip>,<optional port>,<optional listen amount>)
	--Device port: The port of your device which comunicates through serial (eg '/dev/ttyUSB0')
	--baud badnwidth of the serial port. Default: 9600
	--timeout. Time of serial to respond in seconds. Default: 5
	--ip: The ip of your server (eg '192.168.1.4')
	--port: The port of your server (eg 8080)
	--listen: same as socket.listen()
-- startServer()
	--Starts the server & let clients to connect
-- setTimeout()
	--Set the maximum time of a client to respond in seconds. Default: 5 seconds
	--eg server.setTimeout(10)
-- setMode(mode)
	--The mode of the server. Sending raw data from serial read to the client and vice versa or
	   sending html pages from a folder while replacing some html data with serial data
	   mode can be 'raw' for data sending & reiceving directly through serial or 'folder' for
	   interactivity with a folder first. Default is folder
	--eg (server.setMode('raw')
-- setWait(waitTime)
	--In case you are using a very slow baud it is possible to miss some responses from serial.
	--you can use some wait time before retrieve data, as a result you won't loose any details of the response.
	--eg server.setWait(1)
	--you are using seonds and the default is 0
-- setServerDir(directory)
	--Set the root directory of html pages.
	--eg server.setServerDir('/var/www/html')
-- set404(path)
	--Sets the default display page of 404 error messages
	--eg server.set404('/var/www/404.html')
-- parseArgs(boolean)
	--Will pass the aguments of web request to the serial as write if set to true. Default:False
	--eg server.parseArgs(true)
-- chaning 404 error message
	--You can change 404 errors to your own style by chaning the class viariable Error404
	--eg server.Error404 = "<html><body><h1>Error</h1></body></html>"
	--You can also set an html file as an error display by calling server.set404 method
	--eg server.set404('/var/www/html/404_error.html')
-- contentLength(boolean)
	--Enables the content length response header if set to true. Default: False
	--eg server.contentLength(true)
-- Chaning Error Message:
	--you can change the error message response by changing the class variable error_response
	--eg server.error_response = "Error: Somthing is broken!"
	--if you set path to html_error_file the server will send that file instead of the specific message that was set in
	error_response
	--eg server.html_error_file = '/var/www/html/errorfile.html'
-- Suported icon types
	-- You can change the supported icon types of the server by changing the icon_types variable of the class
	--eg server.icon_types = ['jpg','png'].
	--Default:['jpg','png','ico']
-- Response headers
	-- you can change/add/remove the response headers by changing the headers variable of the class. Default:['Connection: closed']
	-- eg server.headers = ['Server: PythontestServer','Connection: closed']


-- Changing Supported methods
   --you can change supported methods by changed the methods variable of the clas
   --eg server.methods = ['GET','HEAD']

Parameters & how html comunicates with serial.
if you have parse arguments enabled then you can put blocks of {{argument name}} to your html. the block will be replaced with the the value of your argument
if you wan't to reiceve data from serial without passing arguments then you must type {{send=WhatToSend}} this will send data to the serial and will replace the block with the response.
if you don't wan't to send data at all but you wan't to reiceve data from html then you can put somthing like that. {{reiceve}}.
if you wan't to send data but don't wait for reiceve. You can try somthing like that {{sendn=Data to send}}

Display user data arguments to html (only)
You can display some (or all) of the data users send to serial by typing {{display=userArgument}} The block will be replaced by the data the user send and not by the serial response.

Keep in mind that blocks may not be replaced if data were not reiceved from serial
"""
import serial
import socket
import os
import time
	
class server:
	__socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	__ip = ''
	__port = 8080
	__listen = 5
	__device = ''
	__timeout = 0
	__okheader = "HTTP/1.1 200 OK\n"
	__404header = "HTTP/1.1 404 Not Found\n"
	__methodNotAllowed = "HTTP/1.1 405 Method Not Allowed\n"
	__mode = 'folder'
	__server_directory = '/var/www/py2serial/'
	__cl = False #content length
	__pa = False #Parse Args
	__waitTime = 0

	methods = ['GET']
	Error404 = "<html><body><h1>Error: 404 Page not Found</h1></body></html>"
	error_response = "<html><body><h1>Error. Bad request</h1></body></html>"
	html_error_file = ""
	headers = ['Connection: closed']
	icon_types = ['jpg','png','ico']
	def set404(self,path):
		try:
			f = open(path,'r')
			self.Error404 = f.read()
			f.close()
		except:
			pass

	def parseArgs(self,togle):
		self.__pa = togle

	def setWait(self,waitTime):
		self.__waitTime = waitTime
		
		
	def contentLength(self,togle):
		self.__cl = togle

	def setServerDir(self,directory):
		d = directory
		if (d[-1] == os.sep):
			d = d[:-1]
		self.__server_directory = d
	def __init__(self,device,baud=9600,time_out=5,ip='',port=8080,listen=5):
		self.__device = device
		self.__baud = baud
		self.__timeout = time_out
		self.__serial = serial.Serial(device,baud,timeout=time_out)
		self.__ip = ip
		self.__port = port
		self.__socket.bind((self.__ip,int(self.__port)))
		self.__socket.listen(self.__listen)
	def send(self,data):
		self.__serial.write(str(data).encode())
		time.sleep(self.__waitTime)
		return self.__serial.read(self.__serial.inWaiting()).decode()
	def sendn(self,data):
		self.__serial.write(str(data).encode())
		return ""
	def recv(self):
		time.sleep(self.__waitTime)
		return self.__serial.read(self.__serial.inWaiting()).decode()

		


	def setTimeout(self,timeout=5):
		self.__timeout = timeout
	def setMode(self,mode):
		self.__mode = mode
	def __initMethods(self):
		newMethods = []
		for i in self.methods:
			newMethods.append(i.lower())
		return newMethods

	def __antiHacking(self,request_file,method):
		print(type(request_file))
		request_file = request_file.lower()
		
		if(request_file.find("..") != -1):
			return True
		if(request_file.find("%00") != -1):
			return True
		if(request_file.find(" ") != -1):
			return True
		if(request_file.find("http") != -1):
			return True
		if(not(method.lower() in self.__initMethods())):
			return True
	def __initHeaders(self):
		headers = ''
		for i in self.headers:
			headers += i + "\n"
		headers +="\n"
		return headers
	def __initArguments(self,arguments):
		try:
			if(arguments.find("?") == -1):
				return ""
			x,y = arguments.split("?")
			if (y.find("&") != -1):
				z = y.split('&')
				return z
			else:
				return y
		except:
			return ""
	def __getType(self,path):
		#print("_getType test")
		if(path.find(".") == -1):
			return "NotFound"
		x = ''		
		for i in range(len(path)):
			if((path[len(path)-i-1:])[0] == '.'):
				break
			x = path[len(path)-i-1:]
		return x
	def __getArgument(self,arg,args):
		value = ''
		if (type(args) is str):
			if(args.find("=") != -1):
				if(args.split("=")[0] == arg or args == arg):
					value = args.split("=")[-1]
			elif(args == arg):
				value = arg
		else:
			for a in args:
				if(a.find("=") != -1):
					if(a.split("=")[0] == arg or a == arg):
						value = a.split("=")[-1]
				elif(a == arg):
					value = arg

		return value
			
			
							

	def __foldersMode(self,request_file):
		
		if (request_file.find("?") != -1):
			request_file_path = request_file.split("?")[0]
		else:
			request_file_path = request_file


		
		isIcon = self.__getType(request_file_path)

		if(isIcon in self.icon_types):
			try:
				fl = open(self.__server_directory+request_file_path,'rb')
			except:
				return 404
			data = fl.read()
			return data
		else:
			try:
				fl = open(self.__server_directory+request_file_path,'r')
			except:
				return 404

		data = fl.read()
		fl.close()
			

		number_of_serials = int(data.count("{{"))
		other_args = []
		request_args = self.__initArguments(request_file)

		x = 0
		for i in range(number_of_serials):
			x += data[x:].find("{{")
			y = data[x:].find("}}") + x
			arg = data[x+2:y]
			print(arg)
			res = ''
			if(arg.find('=') != -1):
				t,a = arg.split('=')
				
				if(t == 'send'):
					res = self.send(a)
					#print(res)
				if(t == 'sendn'):
					res = self.sendn(a)
				if(t == 'display'):
					res = self.__getArgument(a,request_args)
	
						
			else:
				if(arg == 'reiceve'):
					res = self.recv()
				else:
					other_args.append(arg)
					continue #Won't Replace page
				
							
				
			data = data[:x] + res + data[y+2:]
				#print(data)

		if(self.__pa == True):
			x = 0
			request_args = self.__initArguments(request_file)
			number_of_serials = int(data.count("{{"))
			if(number_of_serials == 0 and type(str) is str):
				self.sendn(request_args)
			else:
				not_return_args = request_args
			for i in range(number_of_serials):
				x += data[x:].find("{{")
				y = data[x:].find("}}") + x
				arg = data[x+2:y]
				res = ''
				print(request_args)
				if (request_args != ""):
					if(type(request_args) is str):
						if(request_args.find('=') != -1):
							if(request_args == arg or request_args.split("=")[0] == arg):
								res = self.send(request_args)
							else:
								self.sendn(request_args)
						else:
							if(request_args == arg):
								res = self.send(request_args)
	
						if(res != ''):
							try:
								other_args.remove(arg)
							except:
								#in case you are using the same argument multiple times
								#in your code
								pass
							data = data.replace(data[x:y+2],res)
						continue
					else:
						for a in request_args:
							res = ''
							if(a.find('=') != -1):
								if(a == arg or a.split("=")[0] == arg):
									res = self.send(a)
									not_return_args.remove(a)
				
							else:
								if(a == arg):
									res = self.send(a)
									not_return_args.remove(a)

							if(res != ''):
								try:
									other_args.remove(arg)
								except:
									#in case you are using the same argument multiple times
									#in your code
									pass
								data = data.replace(data[x:y+2],res)
			for i in not_return_args:
				self.sendn(i)
		

			
				
						
	

		return data.encode()
	
	def __rawMode(self,data):
		r = self.send(data)
		return r
		
		
		

	def startServer(self):
		while True:
			c,addr = self.__socket.accept()
			if(self.__timeout>0):
				pass				
				c.settimeout(self.__timeout)
			try:
				headers = c.recv(2048).decode()
			except:
				pass
			#print(headers)
			try:
				method = headers.split(' ')[0]
				request_file = headers.split(' ')[1]
			except:
				method = "GET"
				request_file = "/"

			

			if (request_file == '/'):
				request_file = '/index.html'
			if (request_file[0] == '/' and request_file[1] == '?'):
				request_file = '/index.html' + request_file[1:]

			


			if(self.__antiHacking(request_file,method)):
				
				

				if(self.html_error_file != ""):
					response = open(self.html_error_file,'r').read()
				else:
					response = self.error_response

				responseH = self.__methodNotAllowed
				if(self.__cl):
					responseH += 'Content-Length: '+str(len(response))+'\n'
				responseH += self.__initHeaders()
				data_send = responseH + response
				c.send(data_send.encode())
				c.close()
				continue

			
			if(self.__mode == 'folder'):
				##try:
				respond = self.__foldersMode(request_file)
				##except:
					#respond = 404
				if(respond == 404):# Not found
					responseH = self.__404header
					response = self.Error404.encode()

				else:
					responseH = self.__okheader
					response =respond
			else:
				responseH = self.__okheader
				respond = self.__rawMode(request_file)
				response = respond
			
			#response += "Some raw data"

			
			if(self.__cl):
					responseH += 'Content-Length: '+str(len(response))+'\n'
			responseH += self.__initHeaders()
			
			data_send = responseH.encode() + response
			try:
				c.send(data_send)
			except:
				pass
			try:
				c.close()
			except: 
				pass



