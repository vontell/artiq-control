# An experiment which creates a plot of the time needed to
# detect n photons while applying a 532 nm laser to a room
# temperature NV-center
# Author: Aaron Vontell
# Date: January 12, 2017

from artiq.experiment import *
from rle.pipistrello import Board

class CounterTest(EnvExperiment):

	def build(self):
		
		# Initialize the board
		self.board = Board(self)

	@kernel
	def run(self):
		
		counts = range(5, 6)
		
		for n in counts:
		
			self.board.reset()

			# Start the pulse
			self.board.get_core().break_realtime()

			# Delaying to make sure we don't get initial RTIO Underflow Errors
			print("Beginning test to detect ", n , " photons")
			delay(1*s)
			START = now_mu()
			print("Starting 532 nm pulse at time ", START)
			self.board.ttls[1].on();
			
			# TESTING: TAKE THIS OUT IN THE END
			# A fake photon count to mimic a response
			for i in range(n+1):
				self.board.ttls[0].pulse(2*us)
				delay(2*us)
			
			print("APD beginning to listen at time ", START)

			# next_pulse will be given self.board and the timestamp
			# of the last rising edge. An additional delay of `latency`
			# will also be inserted before calling next_pulse
			window = 10 * us
			self.board.register_rising(0, record, START, window, threshold=n)
			
@kernel			
def record(board, last, start):
	
	delay(50*us)
	board.ttls[1].off()

	#detect_times += (last - start)
	print("Time to detect photons (in mu): ", last-start)