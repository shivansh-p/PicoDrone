#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Auther:   Stanley Huang
# Project:  PicoDrone 0.8
# Date:     2022-11-25
#
'''
The MIT License (MIT)
Copyright (C) 2022 Stanley Huang, huangstan1215@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
'''
from machine import Pin
import time

# MPU-6050 --------------------------------------------------------------------
from machine import I2C
from imu import MPU6050

# R8EF ------------------------------------------------------------------------
import state_machine
from state_machine import R8EF_channel

# ZMR SimonK ------------------------------------------------------------------
from simonk_pwm import ZMR

# Flight Controller -----------------------------------------------------------
from flight_controller import acc_sum_base, acc_sum_escape_g, shutdown, main_loop
from flight_controller import flight_ctr_fr, flight_ctr_fl
from flight_controller import flight_ctr_bl, flight_ctr_br

# debug module ----------------------------------------------------------------
from flight_data import flight_data
bb = flight_data(b_debug=True)


### initializing MPU-6050
bb.write('initializing MPU-6050')
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

### initializing R8EF_channel
bb.write('initializing R8EF channels')
pin16 = Pin(16, Pin.IN, Pin.PULL_UP)
st0 = R8EF_channel(0, state_machine.mark, in_base=pin16, jmp_pin=pin16)
st0.active(1)

pin17 = Pin(17, Pin.IN, Pin.PULL_UP)
st1 = R8EF_channel(1, state_machine.mark, in_base=pin17, jmp_pin=pin17)
st1.active(1)

pin18 = Pin(18, Pin.IN, Pin.PULL_UP)
st2 = R8EF_channel(2, state_machine.mark, in_base=pin18, jmp_pin=pin18)
st2.active(1)

# the value range of the joysticks
st_range = [ # min, mid, max
            [0, 4888, 9928],
            [0, 5031, 9966],
            [0, 4925, 9920],
           ]


### initializing SimonK PWM
bb.write('initializing SimonK')
# min, max, init, limit
m_range_0 = [110, 7800, 50, 8500]
m_range_1 = [215, 5700, 100, 8400]
m_range_2 = [545, 7900, 400, 8700]
m_range_3 = [3750, 6400, 3600, 8700]

motor_0 = ZMR(Pin(6), duty=m_range_0[2])
motor_1 = ZMR(Pin(7), duty=m_range_1[2])
motor_2 = ZMR(Pin(8), duty=m_range_2[2])
motor_3 = ZMR(Pin(9), duty=m_range_3[2])
time.sleep(1.0)
motor_0.duty(m_range_0[0])
motor_1.duty(m_range_1[0])
motor_2.duty(m_range_2[0])
motor_3.duty(m_range_3[0])


### initializing Flight Controllers
bb.write('initializing Flight Controllers')
flight_ctr_0 = flight_ctr_fr('fc0', st_range, m_range_0, debug=bb)
flight_ctr_1 = flight_ctr_fl('fc1', st_range, m_range_1, debug=bb)
flight_ctr_2 = flight_ctr_bl('fc2', st_range, m_range_2, debug=bb)
flight_ctr_3 = flight_ctr_br('fc3', st_range, m_range_3, debug=bb)


### before taking off, initialize PicoDrone
bb.write('before taking off, initialize PicoDrone')
# figuring out the baseline of acc sum 
based_acc_sum = acc_sum_base(imu, bb)
flight_ctr_0.based_acc_sum = based_acc_sum
flight_ctr_1.based_acc_sum = based_acc_sum
flight_ctr_2.based_acc_sum = based_acc_sum
flight_ctr_3.based_acc_sum = based_acc_sum


# figuring out the acc sum at the boundary of escape gravity
es_acc_sum = acc_sum_escape_g(imu, 
                              flight_ctr_0, flight_ctr_1, flight_ctr_2, flight_ctr_3, 
                              motor_0, motor_1, motor_2, motor_3,
                              bb)
flight_ctr_0.es_acc_sum = es_acc_sum
flight_ctr_1.es_acc_sum = es_acc_sum
flight_ctr_2.es_acc_sum = es_acc_sum
flight_ctr_3.es_acc_sum = es_acc_sum

#time.sleep(2.0)

shutdown(imu, 
         flight_ctr_0, flight_ctr_1, flight_ctr_2, flight_ctr_3, 
         motor_0, motor_1, motor_2, motor_3, 
         m_range_0, m_range_1, m_range_2, m_range_3, 
         bb)


### entering the main loop
bb.write('entering the main loop')
main_loop(imu, st0, st1, st2, 
          flight_ctr_0, flight_ctr_1, flight_ctr_2, flight_ctr_3, 
          motor_0, motor_1, motor_2, motor_3,
          bb)
