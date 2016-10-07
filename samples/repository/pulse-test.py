# Tests the connection to the board by flashing each LED light
# Author: Aaron Vontell
# Date: 10-05-2016

from artiq.experiment import *

class LedPulseTest(EnvExperiment):
	def build(self):
		self.setattr_device("core")
		self.setattr_device("ttl0")
		self.setattr_device("led1")
		self.setattr_device("led2")
		self.setattr_device("led3")
		self.setattr_device("led4")

	@kernel
	def run(self):
		self.core.reset()
		
		try:
			self.core.break_realtime()
			self.led1.pulse(250*ms)
			self.led2.pulse(250*ms)
			self.led3.pulse(250*ms)
			self.led4.pulse(250*ms)
			with parallel:
				self.led1.pulse(500*ms)
				self.led2.pulse(500*ms)
				self.led3.pulse(500*ms)
				self.led4.pulse(500*ms)
		except RTIOUnderflow:
			print_underflow()

def print_underflow():
    print("RTIO underflow occured")
