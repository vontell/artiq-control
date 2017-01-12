# An experiment that tests the Pipistrello abstraction
# Author: Aaron Vontell
# Date: January 11, 2017

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
		# (Minimum delay needed between instructions)
		# TODO Why does 64 not work? Seems to be a buffer issue...
		#print("Finding board latency...")
		#latency = self.board.find_latency(4 * us, 63, 50, 2)
		#print("Found latency: ", latency, " sec")
		
		# Start the pulse
		self.board.get_core().break_realtime()
		
		# Delaying to make sure we don't get initial RTIO Underflow Errors
		print("Before delay of 2 seconds: ", now_mu())
		delay(2*s)
		START = now_mu()
		print("Start time: ", START)
		print("Starting pulse")
		# pulse ttl = 0 with a square wave of T = 4 us, and 20 oscillations
		self.board.pulse(0, 4 * us, 20)
		print("Pulses placed. Done!")
        
		# Start listening for rising edge events
		print("Register rising edge event")
		
		# next_pulse will be given self.board and the timestamp
		# of the last rising edge. An additional delay of `latency`
		# will also be inserted before calling next_pulse
		self.board.register_rising(0, next_pulse, START, threshold=3)

@kernel			
def next_pulse(board, start):
	
	#print("Starting new pulse")
	
	#at_mu(start)
	delay(15*us) #30
	
	board.ttls[1].pulse(5 * us)
	delay(5* us)
	board.ttls[1].pulse(5 * us)
	delay(5* us)
	board.ttls[1].pulse(5 * us)
	delay(5* us)
	board.ttls[1].pulse(5 * us)
	delay(5* us)
	board.ttls[1].pulse(5 * us)
	delay(5* us)
	board.ttls[1].pulse(5 * us)
	delay(5* us)
	board.ttls[1].pulse(5 * us)
	delay(5* us)
	board.ttls[1].pulse(5 * us)
	delay(5* us)
	board.ttls[1].pulse(5 * us)
	delay(5* us)
	board.ttls[1].pulse(5 * us)
	delay(5* us)
	board.ttls[1].pulse(5 * us)

	print("Finished new pulse placement")
	