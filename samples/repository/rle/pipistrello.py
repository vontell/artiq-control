# Abstraction of the Pipistrello board to be used for easily creating
# experiments that use the board
# Author: Aaron Vontell
# Date: October 21, 2016

from artiq.experiment import *

class Board:
	
	# Creates a Pipistrello board, where experiment is the class that will
	# provide context for the board.
	def __init__(self, experiment):
		
		self.experiment = experiment
		experiment.setattr_device('core')

        # Set the attributes for each TTL output (0-14)
		
		experiment.setattr_device('ttl0')
		experiment.setattr_device('ttl1')
		experiment.setattr_device('ttl2')
		experiment.setattr_device('ttl3')
		experiment.setattr_device('ttl4')
		experiment.setattr_device('ttl5')
		experiment.setattr_device('ttl6')
		experiment.setattr_device('ttl7')
		experiment.setattr_device('ttl8')
		experiment.setattr_device('ttl9')
		experiment.setattr_device('ttl10')
		experiment.setattr_device('ttl11')
		experiment.setattr_device('ttl12')
		experiment.setattr_device('ttl13')
		experiment.setattr_device('ttl14')
		experiment.setattr_device('ttl15')
		
		self.ttls = [
			experiment.ttl0,
			experiment.ttl1,
			experiment.ttl2,
			experiment.ttl3,
			experiment.ttl4,
			experiment.ttl5,
			experiment.ttl6,
			experiment.ttl7,
			experiment.ttl8,
			experiment.ttl9,
			experiment.ttl10,
			experiment.ttl11,
			experiment.ttl12,
			experiment.ttl13,
			experiment.ttl14,
			experiment.ttl15
		]
		
	# Resets the board This should be called at the start of every 'run'
	# command in your experiment
	def reset(self):
		self.experiment.core.reset()
	
	# Flashes LEDs on the board to test the connection
	def led_test(self):
		pass
		
	# Pulses the FPGA on ttl with a period of period. If no length is given,
	# then the pulse will be continuous. Otherwise, the pulse will occur for
	# length time
	def pulse(ttl, period, length=None):
		half_period = period / float(2)
		
		if length is None:
			while True:
				experiment.delay(half_period)
				self.ttls[ttl].pulse(half_period)
		else:
			raise NotImplementedError
		
	# Returns a string that can be printed when an UnderflowError occurs
	# These errors occur when you run the board at a speed that is too fast
	# for instruction timing to keep up.
	def get_underflow(self):
		return "UnderflowError on Pipistrello Board (your instructions are beginning to overlap)"
		