#!/usr/bin/python
# Author:wu,guoan Guoan.wu@intel.com
# Copyright (c) 2014 Intel Corporation.
# Permission is hereby granted, free of charge, to any person obtainin
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import mraa
import time
import sys
import string
import os
import socket
import json

HOST = "127.0.0.1"
PORT = 41234

def register_metric(metric_name, metric_type):
	msg = {"n": metric_name,"t": metric_type}
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(json.dumps(msg), (HOST, PORT))

def send_data(metric_name, value):
	msg = {"n": metric_name,"v": value}
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(json.dumps(msg), (HOST, PORT))

board = sys.argv[1]
forcecycle = string.atoi(sys.argv[2])
print "board:",board
print "s0ix cycle:", forcecycle
register_metric("plancycle1", "s0ixcycle.v1.0")
register_metric("cycle1", "s0ixcycle.v1.0")
register_metric("plancycle2", "s0ixcycle.v1.0")
register_metric("cycle2", "s0ixcycle.v1.0")
register_metric("cycle3", "s0ixcycle.v1.0")
	
## here is the mapping table and need to get the hardware mapping table from jason file or from the xml file 
if(board == "board1"):
	s0i1=mraa.Aio(0)
	s0i3=mraa.Aio(1)
	pwgd = mraa.Gpio(3)
	pwrbutton = mraa.Gpio(4)
	print "board1 io setup finish"
	## register the plancycle and update the value in this pointer
	send_data("plancycle1", forcecycle)

register_metric("plancycle3", "s0ixcycle.v1.0")
	
elif(board == "board2"):
	s0i1=mraa.Aio(2)
	s0i3=mraa.Aio(3)
	pwgd = mraa.Gpio(5)
	pwrbutton = mraa.Gpio(6)	
	print "board2 io setup finish"
	## register the plancycle and update the value in this pointer
	send_data("plancycle2", forcecycle)


elif(board == "board3"):
	s0i1=mraa.Aio(4)
	s0i3=mraa.Aio(5)
	pwgd = mraa.Gpio(7)
	pwrbutton = mraa.Gpio(8)
	print "board3 io setup finish"
	## register the plancycle and update the value in this pointer
	send_data("plancycle3", forcecycle)

pwgd.dir(mraa.DIR_IN)
pwrbutton.dir(mraa.DIR_OUT)
pwrbutton.write(0)

## 1.8V 
analogvoltagethreshold = 210
def IsVoltageHigh(analog):
	if(analog.read() > analogvoltagethreshold):
		return 1
	return 0

####return: 0--> S0, 1--> s0i1, 3--> s0i3, 4--> off
def system_state():
	if(pwgd.read() == 1 and IsVoltageHigh(s0i1) == 1 and IsVoltageHigh(s0i3)==1):
		return 0
	
	if(pwgd.read()==1 and IsVoltageHigh(s0i1) == 0 and IsVoltageHigh(s0i3)==1):
		return 1		
	
	if(pwgd.read()==1 and IsVoltageHigh(s0i1) == 0 and IsVoltageHigh(s0i3)==0):
		return 3
	
	if(pwgd.read()==0 and IsVoltageHigh(s0i1)==0 and IsVoltageHigh(s0i3)==0):
		return 4

def presspwrbutton(timeout):
	pwrbutton.write(1)
	time.sleep(timeout)
	pwrbutton.write(0)	
	#print "press power button with timeout:", timeout

i=0
str='';
while (i<forcecycle):
	ret=system_state()
	if ret==3: ##system is in s0i3 state
		presspwrbutton(1)
		ret = system_state()
		delay=0
		while(ret!=0x0):
			ret=system_state()
			time.sleep(1)
			delay=delay+1
			if(delay>120):
				break

		i=i+1
		print "current cycle:",i
		if(board == "board1"):
			send_data("cycle1", i)
		elif(board == "board2"):
			send_data("cycle2", i)
		elif(board == "board3"):
			send_data("cycle3",i)
		
		if(delay>120):
			print "system can't resume from s0i3 on cycle:", i
			break
	
	elif ret==0x0 : ## system is in s0.
		time.sleep(1)  
		presspwrbutton(1) 
		ret = system_state()
		delay=0
		while (ret!=0x3): ## system not in s0i3 state
			time.sleep(1)
			ret=system_state()
			delay=delay+1
			if(delay>120):
				break
		if(ret==0x3):
			time.sleep(5)
		if(delay>120):
			print "system can't enter to s0i3 on cycle:", i
			break

#send_data("cycle", 0)
