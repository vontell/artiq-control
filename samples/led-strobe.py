# A simple program that turns an LED on the board on 
# and off every half second
# Author: Aaron Vontell
# Date: 9-28-2016

from artiq.experiment import *

class LED(EnvExperiment):
	def build(self):
		self.setattr_device("core")
		self.setattr_device("led")

	@kernel
	def run(self):
		on = False
		while(True):
			delay(500*s)
			if on:
				on = False
				self.led.off()
			else:
				on = True
				self.led.on()