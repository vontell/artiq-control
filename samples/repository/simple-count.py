def build(self):
    self.setattr_argument("count", NumberValue(ndecimals=0, step=1))

def run(self):
    for i in range(self.count):
        print("Hello World", i)

# A simple program that counts and outputs to terminal
# Author: Aaron Vontell
# Date: 9-28-2016

from artiq.experiment import *

class Count(EnvExperiment):
	def build(self):
	    self.setattr_argument("count", NumberValue(ndecimals=0, step=1))

	def run(self):
	    for i in range(self.count):
	        print("Count: " + str(i), i)