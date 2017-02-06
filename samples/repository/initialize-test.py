# An experiment which creates a plot of the time needed to
# detect n photons while applying a 532 nm laser to a room
# temperature NV-center
# Author: Aaron Vontell
# Date: January 12, 2017

from artiq.experiment import *
from rle.pipistrello import Board
from rle.rabi import RabiExperiment
import matplotlib.pyplot as plt
import numpy as np

class CounterTest(EnvExperiment):

	def build(self):
		
		# Initialize the board and experiment
		self.board = Board(self)
		self.rabi = RabiExperiment(self.board)
		
		self.fake_pulse_window = np.random.exponential(30*us, 20)
		self.fake_pulse_time = np.random.exponential(30*us, 20)
		self.background = np.random.exponential(10 ** -2, 30)
		self.start_delay = np.random.exponential(10*us)
		
		print(self.fake_pulse_window)
		print(self.fake_pulse_time)
		print(self.background)
		print(self.start_delay)
		

	@kernel
	def run(self):

		# The different number of photons to count for
		photon_counts = range(3, 12)

		# The ports / TTL / APD outputs to use
		laser_port = 1
		apd_port = 0

		# True if we want to print out information during the test
		verbose = True
		
		# The timeout function for sweeping
		#@kernel
		#def timeout_fn(n): return 30*us
		
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
		# windows = self.rabi.get_photon_windows(laser_port, apd_port, photon_counts, timeout_fn, windows, self.fake_pulse_window , verbose)

		# Returns a mapping of n (the number of photons to count) to the
		# time it takes from the start of the laser application to the last
		# timestamp of a received photon (which is a photon that is part of a
		# sequence of photons that are captured within a given window, given by windows)
		init_times = self.rabi.get_time_to_detect(laser_port, apd_port, photon_counts, 1, init_times, self.fake_pulse_time, verbose, tolerance=0.5*us)

		print("Finished NV center initialization analysis")
		print("Tested window times (in mu): ", windows)
		print("Initialization time results: ", init_times)
		
		plot_results(photon_counts, windows, init_times, self.fake_pulse_window)

		
def plot_results(photon_counts, windows, init_times, pulse):
	
	# Results for photon window times
	ticks = range(min(photon_counts), max(photon_counts) + 1)
	averages = [n for n in photon_counts]
	mins = [n for n in photon_counts]
	maxs = [n for n in photon_counts]
	xs = [n for n in photon_counts]
	for i in range(len(windows)):
		tup = windows[i]
		n, average, minimum, maximum = tup
		xs[i] = n
		averages[i] = average
		mins[i] = minimum
		maxs[i] = maximum
		
	to_first_photon = [n for n in photon_counts]
	to_last_photon = [n for n in photon_counts]
	time_to_x = [n for n in photon_counts]
	for i in range(len(init_times)):
		tup = init_times[i]
		n, time_first, time_last = tup
		time_to_x[i] = n
		to_first_photon[i] = time_first
		to_last_photon[i] = time_last
	
	wins = plt.figure(1)
	plt.title("Photon Count Window Times")
	plt.xlabel("Window Size (Photons)")
	plt.ylabel("Window Time (ns)")
	plt.xticks(ticks)
	plt.plot(xs, averages, "-r", label="average")
	plt.plot(xs, mins, ":b", label="minimum")
	plt.plot(xs, maxs, "g", label="maximum")
	plt.legend()
	wins.show()
	
	times = plt.figure(2)
	plt.title("Time to Photon Window")
	plt.xlabel("Window Size (Photons)")
	plt.ylabel("Time to Photon (ns)")
	plt.xticks(ticks)
	plt.plot(time_to_x, to_first_photon, "-r", label="Time to first photon")
	plt.plot(time_to_x, to_last_photon, ":b", label="Time to last photon")
	plt.legend()
	times.show()
	
	detected = plt.figure(3)
	plt.title("Approximate Detection")
	plt.xlabel("Time (in us)")
	plt.ylabel("Power (boolean)")
	detect_times = []
	detect_ys =    []
	total = pulse[0]
	for i in range(1, len(pulse)):
		now = pulse[i]
		peak = now + total
		total = peak
		detect_times.append(peak - 0.0000001)
		detect_times.append(peak)
		detect_times.append(peak + 0.0000001)
		detect_ys.append(0)
		detect_ys.append(1)
		detect_ys.append(0)
		
	print(pulse)
	plt.plot(detect_times, detect_ys)
	detected.show()
	
	input("Press enter to exit...") # To Pause