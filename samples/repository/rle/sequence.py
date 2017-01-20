# A structure for holding pulse sequences to be executed by the FPGA board and
# the ARTIQ runtime. Note that this pulse sequence is computed and entered into
# the ARTIQ timeline during runtime (this will change when DMA becomes
# available in ARTIQ 3).
# Author: Aaron Vontell
# Written on Friday January 20th, 2017

from artiq.experiment import Experiment, kernel, us
import numpy as np

class Sequence:
	
	def __init__(self, output, sequence, executions = 1, delay = 0*us):
		'''
		Creates a pulse sequence for later playback on an ARTIQ-enabled board
		`output` - The TTL channel to use as an index for use in pipistrello.py
		`sequence` - The sequence of 'on' and 'off' delays which define the
					 pulse sequence. The sequence starts as off, and the first
					 time represents the delay from `start` (set during the
					 play method) to the first rising edge. The second delay
					 represents the delay from the previous rising edge to the
					 next falling edge. Repeat the process to turn pulses on
					 and off.
		`executions` - An optional parameter defining the number of times that
					   the given pulse sequence should be executed (defaults to
					   1)
		`delay` - The delay between executions of this sequence, if the pulse
				  is repeated
		'''
		
		self.output = output
		self.sequence = sequence
		self.executions = executions
		self.delay = delay
		
	@kernel
	def play(self, start, board):
		'''
		Places the given pulse sequence into the ARTIQ timeline, starting at
		`start`. Includes repetitions if indicated during construction. Plays
		on the given board. Note that this method DOES advance the timeline
		'''
		
		at_mu(start)
		board.ttls[self.output].off()
		for i in range(self.executions):
			is_on = False
			for time_delay in self.sequence:
				delay(time_delay)
				if is_on:
					board.ttls[self.output].off()
					is_on = False
				else:
					board.ttls[self.output].on()
					is_on = True
					
			if self.executions > 1:
				delay(self.delay)