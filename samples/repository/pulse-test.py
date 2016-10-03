# A simple program that runs multiple experiments to determine the maximum
# speed at which our setup can pulse a device
# Author: Aaron Vontell
# Date: 9-30-2016

from artiq.experiment import *

class PulseTest(EnvExperiment):
	def build(self):
		self.setattr_device("core")
		self.setattr_device("ttl0")

	@kernel
	def run(self):
		try:
			for i in range(1000):
				self.ttl0.pulse(1*ns)
				delay(1*ns)
				if i == (1000 - 1):
					print("Finshed test")
		except RTIOUnderflow:
			print_underflow()

def print_underflow():
    print("RTIO underflow occured")
