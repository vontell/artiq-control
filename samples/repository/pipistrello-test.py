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
		
		try:
			
			# pulse ttl = 0 for T = 4 us
			self.board.pulse(0, 4 * us)
			
		except RTIOUnderflow:
			
			print(self.board.get_underflow())