# Tests the connection to the board by flashing each LED light
# Author: Aaron Vontell
# Date: 10-05-2016

from artiq.experiment import *
from rle.pipistrello import Board

class LedPulseTest(EnvExperiment):
	def build(self):
		
		# Initialize the board
		self.board = Board(self)

	@kernel
	def run(self):
		
		self.board.reset()
		self.board.led_test()

def print_underflow():
    print("RTIO underflow occured")
