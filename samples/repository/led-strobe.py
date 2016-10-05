# A simple program that turns an LED on the board on 
# and off every half second
# Author: Aaron Vontell
# Date: 9-28-2016

from artiq.experiment import *

class LED(EnvExperiment):
	def build(self):
		self.setattr_device("core")
		self.setattr_device("led1")

	@kernel
	def run(self):
		self.core.reset()
		s = input_led_state()
		self.core.break_realtime()
		if s:
			self.led1.on()
		else:
			self.led1.off()

def input_led_state() -> TBool:
	return input("Enter desired LED state: ") == "1"