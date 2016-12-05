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
		latency = self.board.find_latency(4 * us, 30, 50, 0)
		print(latency)
		
		self.board.get_core().break_realtime()
		print("Before delay: ", now_mu())
		delay(1*s)
		print("Starting pulse")
		# pulse ttl = 0 for T = 4 us
		self.board.pulse(0, 2 * latency, 20)
		
		print("Pulses placed. Done!")
			
def next_pulse():
	print("Detected pulse!")
