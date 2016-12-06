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
		print("Finding board latency...")
		latency = self.board.find_latency(4 * us, 30, 50, 0)
		print("Found latency: ", latency, " sec")
		
		# Start the pulse sequence
		self.board.get_core().break_realtime()
		print("Before delay of 2 seconds: ", now_mu())
		delay(2*s)
		START = now_mu()
		print("Start time: ", START)
		print("Starting pulse")
		# pulse ttl = 0 for T = 4 us
		self.board.pulse(0, 4 * us, 20)
		print("Pulses placed. Done!")
        
		# Start listening for rising edge events
		print("Register rising edge event")
		self.board.register_rising(0, next_pulse, START)
			
def next_pulse():
	print("Detected pulse!")
