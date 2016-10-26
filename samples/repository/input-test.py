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
                inp.gate_rising(50 * us)
                with sequential:
                    for i in range(11):
                        delay(2 * us)
                        output.pulse(2 * us)
						
			# Prints out the number of rising edges found from the
			# experiment above
            print(inp.count())
        except RTIOUnderflow:

            print_underflow()


# Alerts that underflow occurred

def print_underflow():
    print('RTIO underflow occured')