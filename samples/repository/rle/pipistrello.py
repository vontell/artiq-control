# Abstraction of the Pipistrello board to be used for easily creating
# experiments that use the board
# Author: Aaron Vontell
# Date: October 21, 2016

from artiq.experiment import *
import numpy as np

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
		
		# Set PMTs to input mode
		#self.pmt[0].input()
		#self.pmt[1].input()
        
		self.leds = [
			experiment.led1,
			experiment.led2,
			experiment.led3,
			experiment.led4
		]
		
		# The minimum latency that we have determined for this board for
		# reliable placement of events into the timeline
		self.LATENCY = 2 * us
		self.LATENCY_US = 2 * us
	
	
	# Resets the board This should be called at the start of every 'run'
	# command in your experiment
	@kernel
	def reset(self):
		self.get_core().reset()
        
    
    # Finds the latency associated with placing events into the
    # timeline for this board. Takes as parameters a `max_value` latency
    # which is a starting value for the binary search procedure upper bound,
    # a 'tries' count for the number of tests the board should use
    # for each latency guess, a `timeout` which is the total
    # number of guesses that should be made before the binary search
    # halts, and a `ttl` which is an output that is safe to test on
    #
    # SAVES THIS LATENCY IN CLASS VARIABLE `self.latency`
	@kernel
	def find_latency(self, max_value, tries, timeout, ttl):
		
		total_count = 0
		min_value = 0.0
        
		# Now find the correct value
		while total_count < timeout:
			
			print("Total count: ", total_count)
			self.reset() # Reset any timeline configurations
			delay(1*s)
			guess = (max_value - min_value)/ 2.0 + min_value
			print("Trying with guess: ", guess)
			test_count = 0
			print("[" , min_value , ",", max_value, "]")
			while test_count < tries:
				test_count += 1
				try:
					delay(guess)
					self.ttls[ttl].pulse(guess)
				except RTIOUnderflow:
					print("Failed with guess: ", guess)
					min_value = guess
					break
				except RTIOCollision:
					print("Failed with guess: ", guess)
					min_value = guess
					break
			else:
				print("Succeeded with guess below")
				print(guess)
				max_value = guess
            
			total_count += 1
			
		self.LATENCY = max_value
		return max_value
	
	# Flashes LEDs on the board to test the connection
	@kernel
	def led_test(self):
			
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
	# length iterations
	@kernel
	def pulse(self, ttl, period, length):
		half_period = period / float(2)
		print("Pulse starts at ", now_mu())
		count = 0
		while count < length:
			self.ttls[ttl].pulse(half_period)
			delay(half_period)
			count += 1
		print("Pulse end at ", now_mu())

	
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
	def register_rising(self, pmt, handler, start, threshold=0):
		
		# Set the timeline pointer to start
		at_mu(start)
		
		# Starting now, begin detecting rising edges
        self.pmt[pmt]._set_sensitivity(1)
			
		count = 0
		last = 0
		while True:
			last = self.pmt[pmt].timestamp_mu()
			if last > 0:
				count += 1
				if count > threshold:
					at_mu(last)
					delay(self.LATENCY)
					handler()
					break
			
		
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
	def print_underflow(self):
		print("UnderflowError on Pipistrello Board (your instructions are beginning to overlap)")
		
