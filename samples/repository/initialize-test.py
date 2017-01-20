# An experiment which creates a plot of the time needed to
# detect n photons while applying a 532 nm laser to a room
# temperature NV-center
# Author: Aaron Vontell
# Date: January 12, 2017

from artiq.experiment import *
from rle.pipistrello import Board
from rle.rabi import RabiExperiment
from addict import Dict

class CounterTest(EnvExperiment):

	def build(self):
		
		# Initialize the board and experiment
		self.board = Board(self)
		self.rabi = RabiExperiment(self.board)

	@kernel
	def run(self):

		# The different number of photons to count for
		photon_counts = range(5, 7)

		# The ports / TTL / APD outputs to use
		laser_port = 0
		apd_port = 0

		# True if we want to print out information during the test
		verbose = True
		
		# The timeout function for sweeping
		@kernel
		def timeout_fn(n): return 30*us
		
		# Array to store the window results in
		# Note that this must be a preallocated array!
		windows = [(n, 0, 0, 0) for n in photon_counts]
				  # n, average, min, max in machine units
		
		# Array to store the init time results in
		# Note that this must be a preallocated array!
		init_times = [(n, 0, 0) for n in photon_counts]
				     # n, time from laser start to first photon, time from laser start to last photon
		

		# Returns a mapping of n (the number of photons to count) to the 
		# (average, smallest, largest, we will need to decide) window size
		# needed to get that photon count
		# Take in timeout_fn, which is a function which, given n, returns
		# the amount of time we should test / sweep for to assess this window
		windows = self.rabi.get_photon_windows(laser_port, apd_port, photon_counts, timeout_fn, windows, verbose)

		# Returns a mapping of n (the number of photons to count) to the
		# time it takes from the start of the laser application to the last
		# timestamp of a received photon (which is a photon that is part of a
		# sequence of photons that are captured within a given window, given by windows)
		#init_times = self.rabi.get_time_to_detect(laser_port, apd_port, photon_counts, windows, 1, init_times, verbose)

		print("Finished NV center initialization analysis")
		print("Tested window times (in mu): ", windows)
		print("Initialization time results: ", init_times)

		# Then graph the results