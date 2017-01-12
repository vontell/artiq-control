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
		latency = self.board.find_latency(4 * us, 63, 50, 2)
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
		self.board.register_rising(0, next_pulse, START, threshold=5)
		
		# Make sure to stop the listener
		#self.board.unregister_rising(0)
		#print("Terminated rising edge listener")

@kernel
def next_pulse(board, start):
	
	at_mu(start)
	#delay(1*s)
	delay(8*ns)
	board.ttls[1].pulse(5*ns)
	
	print("Finished new pulse placement: ", now_mu())
