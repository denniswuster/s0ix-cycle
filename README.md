# s0ix-cycle
edison control the mobile device for s0x cycling

HW connection:
1. The system state are indicated from the board with specific signal
2. monitor these signals from the edison IO port
3. Edison according the signal to get the system state
4. According the system state to do the transition. 

S0x Cycle BKM:
1.	Edison monitor board signals raw data to get system state
2.	If the system state is S0, Edison control power button and let the system enter to S0I3
3.	If the system enter to S0I3, wait for 5s, Edison control power button to resume the system from S0I3.
4.	If the system state return back to S0, keep in S0 for 5s and repeat 2~3 steps for specific cycle  

system State: System State Sensor Program:
In Edison, “System State Senor Program” is a services which always run background in Edison to get the raw data of the IO input and determine the power states which are delivered to the IOT dashboard. In Fig3. Power state will transit from the S0 (value is 0) to S0I3 (value is 3) when we do the power cycle transition. Idle time, system will stay in S0 state. 

system Input: Power Control Program
“Power Control Program” implements the “Power State Cycle BKM” which control the platform power button to let the system transit between S0 and S0I3. This program also post the “plan cycle” and “executed cycle” to the IOT dashboard. In Fig 3, we plan 10 cycles of power transition twice and execution is normally each time, then we plan 5 cycles and observe system keep on S0 state after 2 cycles that means the system can’t enter to S0I3 or system already hang. In this case, we need take a look on this platform to see what’s really happened. 

OT Actuation: Deploy the Power Cycle Test 
Edison IOT platform support remote actuation that we can light on/off a LED, reset platforms, run specific cases remotely. In Fig 4, we have one action that let the platform1 to control the power cycle for 1000 times, once we send the action, Edison will get the message to start the “Power Control Program” to do power cycle test for 1000 cycles.  


