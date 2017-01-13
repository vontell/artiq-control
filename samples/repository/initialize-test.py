# An experiment which creates a plot of the time needed to
# detect n photons while applying a 532 nm laser to a room
# temperature NV-center
# Author: Aaron Vontell
# Date: January 12, 2017

from artiq.experiment import *
from rle.pipistrello import Board
from rle.rabi import RabiExperiment

class CounterTest(EnvExperiment):

	def build(self):
		
		# Initialize the board
		self.board = Board(self)

	@kernel
	def run(self):
		
		def window_fn(n: int) -> float:
			return 10*us
		
		photon_counts = range(0, 10)
		laser_port = 0
		apd_port = 0
		verbose = True
		
		rabi = RabiExperiment(self.board)
		print(rabi)
		
		#windows = rabi.get_photon_windows()
		#init_times = rabi.get_time_to_detect(laser_port, apd_port, photon_counts, window_fn, verbose)
		
		print("Finished NV center initialization analysis")
		#print("Initialization time results: ", init_times)