#!/usr/bin/python
#copyright (c) 2014, Intel Corporation
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import socket
import mraa
import json
import os
import string
import errno
import sys
import shlex, subprocess

UDP_IP = "127.0.0.1"
UDP_PORT = 41235

def register_metric(metric_name, metric_type):
	msg = {"n": metric_name,"t": metric_type}
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(json.dumps(msg), (UDP_IP, UDP_PORT))


def send_data(metric_name, value):
	msg = {"n": metric_name,"v": value}
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(json.dumps(msg), (UDP_IP, UDP_PORT))

## register the "component" platform and update the value in this pointer
#register_metric("s0i3cycle1", "platformctrl.v1.0")
register_metric("s0i3cycle1", "platformctrl.v1.2")

# Sensor and parameter names to listen for
componentName = "s0i3cycle1"
sensorName1 = "RESET"
sensorName2 = "S0i3Cycle-1"
sensorName3 = "S0i3Cycle-2"
sensorName4 = "S0i3Cycle-4"

#myLed = mraa.Gpio(13)  #LED hooked up to digital pin 13 (or built in pin on Galileo Gen1 & Gen2)
#myLed.dir(mraa.DIR_OUT)    #set the gpio direction to output

#Sensor and parameter names to listen for
#componentName = "pwrctrl"
#sensorName = "LED"

# Bind to UDP port 41235
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

print "Listening on port", UDP_PORT

"""
def pid_exists(pid):
		if pid < 0:
				return False
		if pid == 0:
				# According to "man 2 kill" PID 0 refers to every process
				# in the process group of the calling process.
				# On certain systems 0 is a valid PID but we have no way
				# to know that in a portable fashion.
				raise ValueError('invalid PID 0')
		try:
				os.kill(pid, 0)
		except OSError as err:
				if err.errno == errno.ESRCH:
						# ESRCH == No such process
						return False
				elif err.errno == errno.EPERM:
						# EPERM clearly means there's a process to deny access to
						return True
				else:
						# According to "man 2 kill" possible error values are
						# (EINVAL, EPERM, ESRCH)
						raise
		else:
				return True
#pid = -1
"""

commandstr=''
ps_board1=0
ps_board2=0
ps_board3=0
while True:
	data,addr = sock.recvfrom(4096)
	print "Received ", data, "from", addr[0]
	if addr[0] != "127.0.0.1":
			print "Rejecting external UDP message from", addr[0]
			continue
	js = json.loads(data)
	component = js["component"]
	command = js["command"]
	argvArray = js["argv"]
	if component == componentName:
			for argv in argvArray:
					name = argv['name']
					value = argv['value']
					print "name: " + name
					print "value: " + value
					if (name == sensorName1):
						print "reset", value
					if (name == sensorName2):
						if ps_board1==0 or (ps_board1 != 0 and ps_board1.poll()) != None:
							commandstr="python ST_STABLITY_S0x_CYCLE.py board1 "+ bytes(value) +" >board1.txt 2>&1 &"
							args = shlex.split(commandstr)
							ps_board1 = subprocess.Popen(args)
							# Wait until process terminates
							print "process id is:",ps_board1.pid
					if (name == sensorName3):
						if ps_board2==0 or (ps_board2 != 0 and ps_board2.poll()) != None:
							commandstr="python ST_STABLITY_S0x_CYCLE.py board2 "+ bytes(value) +" >board1.txt 2>&1 &"
							args = shlex.split(commandstr)
							ps_board2 = subprocess.Popen(args)
							# Wait until process terminates
							print "process id is:",ps_board2.pid
					if (name == sensorName4):
						if ps_board3==0 or (ps_board3 != 0 and ps_board3.poll()) != None:
							commandstr="python ST_STABLITY_S0x_CYCLE.py board3 "+ bytes(value) +" >board1.txt 2>&1 &"
							args = shlex.split(commandstr)
							ps_board3 = subprocess.Popen(args)
							# Wait until process terminates
							print "process id is:",ps_board3.pid
