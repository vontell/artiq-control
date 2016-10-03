# A simple program that turns an LED on the board on 
# and off every half second
# Author: Aaron Vontell
# Date: 9-28-2016

from artiq.experiment import *

class LED(EnvExperiment):
	def build(self):
		self.setattr_device("core")
		self.setattr_device("USER_LED_1")

	@kernel
	def run(self):
		on = False
		while(True):
			delay(500*ms)
			if on:
				on = False
				self.USER_LED_1.off()
			else:
				on = True
				self.USER_LED_1.on()