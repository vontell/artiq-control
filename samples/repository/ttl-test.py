#!/usr/bin/python
# -*- coding: utf-8 -*-
# Takes a TTL output and frequency as arguments,
# and pulses that output until terminated
# Author: Aaron Vontell
# Date: 10-06-2016

from artiq.experiment import *


class TTLTest(EnvExperiment):

    def build(self):
        self.setattr_device('core')

        # Set the attributes for each TTL output (0-14)

        self.setattr_device('ttl0')
        self.setattr_device('ttl1')
        self.setattr_device('ttl2')
        self.setattr_device('ttl3')
        self.setattr_device('ttl4')
        self.setattr_device('ttl5')
        self.setattr_device('ttl6')
        self.setattr_device('ttl7')
        self.setattr_device('ttl8')
        self.setattr_device('ttl9')
        self.setattr_device('ttl10')
        self.setattr_device('ttl11')
        self.setattr_device('ttl12')
        self.setattr_device('ttl13')
        self.setattr_device('ttl14')
        self.setattr_device('ttl15')

        self.ttls = [
            self.ttl0,
            self.ttl1,
            self.ttl2,
            self.ttl3,
            self.ttl4,
            self.ttl5,
            self.ttl6,
            self.ttl7,
            self.ttl8,
            self.ttl9,
            self.ttl10,
            self.ttl11,
            self.ttl12,
            self.ttl13,
            self.ttl14,
            self.ttl15
            ]

        # Grab arguments for choosing the TTL and frequency

        self.setattr_argument('ttl', NumberValue(ndecimals=0, step=1))

        # self.setattr_argument("freq", NumberValue(unit='MHz'))

    @kernel
    def run(self):
        self.core.reset()
        try:

            # Determine the frequency
            # frequency = self.freq * MHz

            # Grab the correct ttl output

            output = self.ttls[self.ttl]

            # Pulse the ttl

            for i in range(100000000):
                delay(2 * us)
                output.pulse(2 * us)
        except RTIOUnderflow:

            print_underflow()


# Alerts that underflow occurred

def print_underflow():
    print('RTIO underflow occured')



			