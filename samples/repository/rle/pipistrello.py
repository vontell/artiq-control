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

        # Set the attributes for each TTL output (0-14), PMT input, and LED
		
		experiment.setattr_device('pmt0')
		experiment.setattr_device('pmt1')
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
		experiment.setattr_device("led1")
		experiment.setattr_device("led2")
		experiment.setattr_device("led3")
		experiment.setattr_device("led4")
		
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
		
		self.pmt = [
			experiment.pmt0,
			experiment.pmt1
		]
        
		self.leds = [
			experiment.led1,
			experiment.led2,
			experiment.led3,
			experiment.led4
		]
		
		# The minimum latency that we have determined for this board for
		# reliable placement of events into the timeline
		self.LATENCY = 2 * us
		
	# Resets the board This should be called at the start of every 'run'
	# command in your experiment
	@kernel
	def reset(self):
		self.get_core().reset()
	
	# Flashes LEDs on the board to test the connection
	@kernel
	def led_test(self):
			self.get_core().break_realtime() # TODO: Determine if this is necessary
			self.leds[0].pulse(250*ms)
			self.leds[1].pulse(250*ms)
			self.leds[2].pulse(250*ms)
			self.leds[3].pulse(250*ms)
			with parallel:
				self.leds[0].pulse(500*ms)
				self.leds[1].pulse(500*ms)
				self.leds[2].pulse(500*ms)
				self.leds[3].pulse(500*ms)
		
	# Pulses the FPGA on ttl with a period of period. If no length is given,
	# then the pulse will be continuous. Otherwise, the pulse will occur for
	# length time
	@kernel
	def pulse(self, ttl, period, length=None):
		half_period = period / float(2)
		
		if length is None:
			while True:
				self.ttls[ttl].pulse(half_period)
				delay(half_period)
		else:
			raise Exception('Not yet implemented!')
	
	# Fires a method (handler) when the count of rising edges on a given PMT
	# input pmt reaches a certain threshold (which defaults to 0). Returns
	# this board for chaining capabilities. Optionally allows for defining
	# the start time to begin listening (defaults to now), and the amount of
	# time to listen for (defaults to forever)
	#
	# NOTE: Make sure to call unregister_rising() to reset the PMT once done
	# 	    This method will call unregister_rising() when the threshold is
	#		reached, but this event may never occur
	@kernel
	def register_rising(self, pmt, handler, threshold=0, start=0, length=0*us):
		
		# Make sure that this pmt is in input mode (and throws an exception
		# if this PMT is not input capable)
		self.pmt[pmt].input()
		
		# Set the timeline pointer to start
		if start == 0:
			start = now_mu()
		at_mu(start)
		
		# Starting now, begin detecting rising edges for the desired length
		# (or forever)
		if length != 0 * us:
			self.pmt[pmt].gate_rising(length)
		else:
			self.pmt[pmt]._set_sensitivity(1)
			
		received = self.pmt[pmt].timestamp_mu()
		
		if received > 0:  # pulse received during gate
			at_mu(received + self.LATENCY)
			handler()
		
	# Unregisters the given pmt from listening for rising edges by turning
	# the input off at an unspecified later date
	@kernel
	def unregister_rising(self, pmt):
		self.pmts[pmt]._set_sensitivity(0)
	
	
	# Returns the core device, in situations where granular control is
	# necessary
	@kernel
	def get_core(self):
		return self.experiment.core
        
	# Returns a string that can be printed when an UnderflowError occurs
	# These errors occur when you run the board at a speed that is too fast
	# for instruction timing to keep up.
	def get_underflow(self):
		return "UnderflowError on Pipistrello Board (your instructions are beginning to overlap)"
		