#!/usr/bin/python
# -*- coding: utf-8 -*-
# In parallel, pulses a signal on TTL0, and reads the signal
# as input from TTL1
# Author: Aaron Vontell
# Date: 10-26-2016

from artiq.experiment import *


class InputTest(EnvExperiment):

    def build(self):
        self.setattr_device('core')

        # Set the attributes for each TTL output (0-14)

        self.setattr_device('ttl0')
        self.setattr_device('ttl1')
        self.setattr_device('pmt0')

    @kernel
    def run(self):
        self.core.reset()
        try:
            
			# Grab and instantiate the relevant inputs and outputs
            output = self.ttl0
            inp = self.pmt0
            inp.input()

            # Pulse the ttl and read as input
            self.core.break_realtime()
            with parallel:
				
				# Continuously read for rising inputs
                inp.gate_rising(10000000 * us)
				
				# Create a pulse sequence to read
                with sequential:
                    for i in range(10000):
                        if (inp.count() > 0):
                            print("Passed count threshold")
                            break
                        delay(2 * us)
                        output.pulse(2 * us)
						
				# Continuously monitor for rising edges
                while True:
                    pass
						
        except RTIOUnderflow:

            print_underflow()

# Alerts that underflow occurred

def print_underflow():
    print('RTIO underflow occured')