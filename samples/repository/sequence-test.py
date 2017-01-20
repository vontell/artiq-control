# Testing and example for the pulse sequence structure in `rle/sequence.py`
# Author: Aaron Vontell
# Written on Friday January 20th, 2017

from artiq.experiment import *
from rle.pipistrello import Board
from rle.sequence import Sequence

class SequenceTest(EnvExperiment):

	def build(self):
		
		# Initialize the board
		self.board = Board(self)
		
		# Define the sequence
		# Note that pre-allocated arrays must be used!
		#         __2us__--3us--_2us_--5us-_2us_-7us--_off
		sequence = [2*us, 3*us, 2*us, 5*us, 2*us, 7*us]
		self.pulse_seq = Sequence(0, sequence, 5, 3*us)

	@kernel
	def run(self):
		
		self.board.reset()

		delay(1*s)
		
		self.pulse_seq.play(now_mu(), self.board)