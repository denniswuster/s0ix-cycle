#!/bin/sh
systemctl start iotkit-agent
python systemstate_sensorupdate.py board1 &
python systemstate_sensorupdate.py board2 &
python systemstate_sensorupdate.py board3 &
python IoTkitActuation.py &