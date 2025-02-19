#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Auther:   Stanley Huang
# Project:  PicoDrone 0.7
# Date:     2022-11-25
#
# ZMR SimonK initialization and control
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
from machine import PWM

class ZMR():
    def __init__(self, pin, freq=50, duty=0):
        self.pwm = PWM(pin)
        self.pwm.freq(freq)
        self.pwm.duty_u16(duty)
    
    def duty(self, duty):
        self.pwm.duty_u16(duty)


def test_zmrs():
    from machine import Pin
    import time
    motor_0 = ZMR(Pin(6))
    motor_1 = ZMR(Pin(7))
    motor_2 = ZMR(Pin(8))
    motor_3 = ZMR(Pin(9))
    m0 = m1 = m2 = m3 = 0
    while True:
        the_input = input("輸入馬達 PWM Duty Cycle: (例如: a30) ")
        if len(the_input)>1:
            duty = int(the_input[1:])
            if the_input[0] == 'a':
                m0 = int(duty)
            elif the_input[0] == 'b':
                m1 = int(duty)
            elif the_input[0] == 'c':
                m2 = int(duty)
            elif the_input[0] == 'd':
                m3 = int(duty)
        print(m0, m1, m2, m3)
        motor_0.duty(m0)
        motor_1.duty(m1)
        motor_2.duty(m2)
        motor_3.duty(m3)
        time.sleep(0.2)


if __name__=='__main__':
    test_zmrs()
