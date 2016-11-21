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
		
		#try:
			
		# flash the board to confirm connection
		self.board.led_test()
		print("Placed led events")
		# pulse ttl = 0 for T = 4 us, and detect the rising edges
		with parallel:
			self.board.register_rising(0, next_pulse, length=10000 * us)
			print("Placed register rising event")
			self.board.pulse(0, 4 * us)
			print("Placed pulse event")
			
		#except RTIOUnderflow:
			
			#print(RTIOUnderflow)
			#self.board.print_underflow()
			
def next_pulse():
	print("Detected pulse!")
