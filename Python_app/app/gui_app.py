import eel
import serial
import time
import sys
import glob

port_Error = False
current_port = None

data = [0, 0, 0, 0, 0, 0, 0, 0]


# Checks for available ports
def serial_ports():
	if sys.platform.startswith('win'):
		ports = ['COM%s' % (i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# This excludes your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')

	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except (OSError, serial.SerialException):
			pass
	return result


def gether_data(data):
	data_string = ''
	for i in range(8):
		data_string += str(data[i]) + ' '
	print("{" + data_string + "}")
	arduino.write(bytes(data_string, 'utf-8'))		# Sample put strip blue 
	time.sleep(0.15)


@eel.expose
def ports_availabe():
	global ports, arduino, port_Error, current_port
	try:
		arduino.close()
		ports = serial_ports()
		if len(ports) == 0:
			raise AssertionError
		elif current_port not in ports:
			current_port = ports[0]
			arduino = serial.Serial(port=str(current_port), baudrate=9600, timeout=.1)
		else:
			arduino = serial.Serial(port=str(current_port), baudrate=9600, timeout=.1)
	except:
		port_Error = True
	
	if current_port == None:
		return 1

	message = "There are ports: "
	num = len(ports) - 1
	for i in range(len(ports)):
		if num >= 1:
			message += str(ports[i]) + ", "
			num -=1
		else:
			message += str(ports[i])
		
	message += "\nCurrently used: " + str(current_port)
	return message



@eel.expose
def get_set_color(color):
	global data
	data[0] = 10
	data[2] = int(color[1:3], 16)
	data[3] = int(color[3:5], 16)
	data[4] = int(color[5:7], 16)
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]


@eel.expose
def get_rainbow(speed, size):
	global data
	data[0] = 3
	data[1] = speed
	data[2] = size
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]



@eel.expose
def get_gradient(color1, color2):
	global data
	data[0] = 2
	data[2] = int(color1[1:3], 16)
	data[3] = int(color1[3:5], 16)
	data[4] = int(color1[5:7], 16)
	data[5] = int(color2[1:3], 16)
	data[6] = int(color2[3:5], 16)
	data[7] = int(color2[5:7], 16)
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]



@eel.expose
def get_strobe(color, speed):
	global data
	data[0] = 11
	data[1] = speed
	data[2] = int(color[1:3], 16)
	data[3] = int(color[3:5], 16)
	data[4] = int(color[5:7], 16)
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]



@eel.expose
def get_police_siren(speed, siren_type):
	global data
	data[0] = 4
	data[1] = speed
	data[2] = siren_type
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]


@eel.expose
def get_matrix(color, speed):
	global data
	data[0] = 12
	data[1] = speed
	data[2] = int(color[1:3], 16)
	data[3] = int(color[3:5], 16)
	data[4] = int(color[5:7], 16)
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]


@eel.expose
def get_brightness(val):
	global data
	data[0] = 0
	data[1] = val
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]


@eel.expose
def set_port(user_port):
	global current_port, arduino
	try:
		arduino.close()
	except:
		return 1
	if user_port not in ports:
		return 1
	else:
		current_port = user_port
		arduino = serial.Serial(port=str(current_port), baudrate=9600, timeout=.1)


@eel.expose
def get_set_preset_color1(color):
	global data
	data[0] = 13
	data[2] = int(color[1:3], 16)
	data[3] = int(color[3:5], 16)
	data[4] = int(color[5:7], 16)
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]

@eel.expose
def get_set_preset_color2(color):
	global data
	data[0] = 14
	data[2] = int(color[1:3], 16)
	data[3] = int(color[3:5], 16)
	data[4] = int(color[5:7], 16)
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]

@eel.expose
def get_set_preset_color3(color):
	global data
	data[0] = 15
	data[2] = int(color[1:3], 16)
	data[3] = int(color[3:5], 16)
	data[4] = int(color[5:7], 16)
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]


@eel.expose
def set_preset_color1():
	global data
	data[0] = 13
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]

@eel.expose
def set_preset_color2():
	global data
	data[0] = 14
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]

@eel.expose
def set_preset_color3():
	global data
	data[0] = 15
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]


@eel.expose
def get_gradient_preset1(color1, color2):
	global data
	data[0] = 16
	data[2] = int(color1[1:3], 16)
	data[3] = int(color1[3:5], 16)
	data[4] = int(color1[5:7], 16)
	data[5] = int(color2[1:3], 16)
	data[6] = int(color2[3:5], 16)
	data[7] = int(color2[5:7], 16)
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]

@eel.expose
def get_gradient_preset2(color1, color2):
	global data
	data[0] = 17
	data[2] = int(color1[1:3], 16)
	data[3] = int(color1[3:5], 16)
	data[4] = int(color1[5:7], 16)
	data[5] = int(color2[1:3], 16)
	data[6] = int(color2[3:5], 16)
	data[7] = int(color2[5:7], 16)
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]


@eel.expose
def set_preset_gradient1():
	global data
	data[0] = 16
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]

@eel.expose
def set_preset_gradient2():
	global data
	data[0] = 17
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]


@eel.expose
def get_rainbow_preset1(speed, size):
	global data
	data[0] = 18
	data[1] = speed
	data[2] = size
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]

@eel.expose
def get_rainbow_preset2(speed, size):
	global data
	data[0] = 19
	data[1] = speed
	data[2] = size
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]


@eel.expose
def set_preset_rainbow1():
	global data
	data[0] = 18
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]

@eel.expose
def set_preset_rainbow2():
	global data
	data[0] = 19
	gether_data(data)
	data = [0, 0, 0, 0, 0, 0, 0, 0]



try:
	ports = serial_ports()
	current_port = ports[0]
	arduino = serial.Serial(port=str(current_port), baudrate=9600, timeout=.1)
except:
	port_Error = True



eel.init('D:\Arduino\LedStrip\Python_app\web') # Needed full path to folder

try:
	eel.start('html/index.html', host='localhost', size=(500, 620))
except:
	if port_Error:
		print("End of program, with invalid port Error")
	else:
		arduino.close()
		print("End of program")
	