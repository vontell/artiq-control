# A simple program that counts and outputs the count to the terminal
# Author: Aaron Vontell
# Date: 9-28-2016

from artiq.experiment import *

class Count(EnvExperiment):
	def build(self):
		self.setattr_device("core")
		self.setattr_argument("count", NumberValue(ndecimals=0, step=1))

	@kernel
	def run(self):
		for i in range(self.count):
			print(i)