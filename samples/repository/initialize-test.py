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

	def run(self):

		# The different number of photons to count for
		photon_counts = range(10, 11)

		# The ports / TTL / APD outputs to use
		laser_port = 0
		apd_port = 0

		# True if we want to print out information during the test
		verbose = True

		# Start the experiments
		rabi = RabiExperiment(self.board)

		# Returns a mapping of n (the number of photons to count) to the 
		# (average, smallest, largest, we will need to decide) window size
		# needed to get that photon count
		# Take in timeout_fn, which is a function which, given n, returns
		# the amount of time we should test / sweep for to assess this window
		windows = rabi.get_photon_windows(laser_port, apd_port, photon_counts, timeout_fn, verbose)
		windows = {10: 5*us}
		

		# Returns a mapping of n (the number of photons to count) to the
		# time it takes from the start of the laser application to the last
		# timestamp of a received photon (which is a photon that is part of a
		# sequence of photons that are captured within a given window, given by windows)
		init_times = rabi.get_time_to_detect(laser_port, apd_port, photon_counts, windows, verbose)

		print("Finished NV center initialization analysis")
		print("Tested window times: ", windows)
		print("Initialization time results: ", init_times)

		# Then graph the results