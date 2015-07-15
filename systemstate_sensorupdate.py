# Copyright (c) 2012, Intel Corporation
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
import mraa
import os
import socket
import json
import time
import sys

HOST = "127.0.0.1"
PORT = 41234
INTERVAL = 2

board = sys.argv[1]
print "board:",board

def register_metric(metric_name, metric_type):
	msg = {"n": metric_name,"t": metric_type}
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(json.dumps(msg), (HOST, PORT))


def send_data(metric_name, value):
	msg = {"n": metric_name,"v": value}
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(json.dumps(msg), (HOST, PORT))
	
register_metric("status1", "s0ixcycle.v1.0")
register_metric("status2", "s0ixcycle.v1.0")
register_metric("status3", "s0ixcycle.v1.0")

if(board == "board1"):
	##get the definition from xml
	s0i1=mraa.Aio(0)
	s0i3=mraa.Aio(1)
	pwgd = mraa.Gpio(3)
	print "board1 io setup finish"

	
elif(board == "board2"):
	s0i1=mraa.Aio(2)
	s0i3=mraa.Aio(3)
	pwgd = mraa.Gpio(5)
	print "board2 io setup finish"
	
elif(board == "board3"):
	s0i1=mraa.Aio(4)
	s0i3=mraa.Aio(5)
	pwgd = mraa.Gpio(7)
	print "board3 io setup finish"

pwgd.dir(mraa.DIR_IN)

## 1.8V 
analogvoltagethreshold = 210
def IsVoltageHigh(analog):
	if(analog.read() > analogvoltagethreshold):
		return 1
	return 0

def system_state():
	if(pwgd.read() == 1 and IsVoltageHigh(s0i1) == 1 and IsVoltageHigh(s0i3)==1):
		return 0
	
	if(pwgd.read()==1 and IsVoltageHigh(s0i1) == 0 and IsVoltageHigh(s0i3)==1):
		return 1		
	
	if(pwgd.read()==1 and IsVoltageHigh(s0i1) == 0 and IsVoltageHigh(s0i3)==0):
		return 3
	
	if(pwgd.read()==0 and IsVoltageHigh(s0i1)==0 and IsVoltageHigh(s0i3)==0):
		return 4

next_send_time = 0
##print "before while.."
while True:
	t = time.time()
	##print "t:",t
	##print "next_send_time:",next_send_time
	if t > next_send_time:
		ret = system_state()
		##print "system state is:",ret
		if(board == "board1"):
			send_data("status1", ret)
		elif(board == "board2"):
			send_data("status2", ret)
		elif(board == "board3"):
			send_data("status3",ret)
		next_send_time = t + INTERVAL
	time.sleep(1)

