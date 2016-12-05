# An experiment that tests the Pipistrello abstraction
# Author: Aaron Vontell
# Date: October 21, 2016

from artiq.experiment import *
from rle.pipistrello import Board


class PipistrelloTest(EnvExperiment):

	def build(self):
		
		# Initialize the board
		self.board = Board(self)

	@kernel
	def run(self):
		
		self.board.reset()
		
		# flash the board to confirm connection
		self.board.led_test()
        
        # Find the latency of this board
		latency = self.board.find_latency(4 * ms, 30, 20, 0)
		print(latency)
		
		'''
		time = now_mu()
		# pulse ttl = 0 for T = 4 us, and detect the rising edges
		self.board.pulse(0, 4 * us, 300)
		
		at_mu(time)
		self.board.register_rising(0, next_pulse, length=10000 * us)
		print("Placed register rising event")
		
		#self.board.reset()
		#
		'''
			
def next_pulse():
	print("Detected pulse!")
