# Configurable tests and experiments for Rabi oscillations
# in Nitrogen Vacancy Centers. 

from artiq.experiment import kernel, s, us
import numpy as np

class RabiExperiment:
  
	def __init__(self, board):
		
		self.board = board
		
	@kernel
	def get_photon_windows(self, laser_port, apd_port, photon_counts, timeout_fn, results, verbose):
		
		print("Beginning initialization window analysis")
		
		for ind in range(len(photon_counts)):
			
			n = photon_counts[ind]
			if verbose: print("Beginning test to get the window time for ", n, " photons")
			
			# Get the sweep timeout before working with the timeline
			timeout = timeout_fn(n)
			
			# Reset the board and timeline, delaying to avoid RTIOUnderflow Errors
			self.board.reset()
			self.board.get_core().break_realtime()
			delay(1*s) # Change this as needed, this is to avoid real time running into the cursor
			
			start = now_mu()
			
			# Make a fake pulse
			self.board.pulse(0, 0.5 * us, 50)
			
			timestamps = [0 for i in range(60)]
			timestamps = self.board.record_rising(apd_port, start, timeout, timestamps)
			
			# Get raw windows
			# CHECK WHEN TIMESTAMPS < WINDOWS SIZE
			windows = [0 for i in range(len(timestamps) - n)]
			for i in range(len(timestamps) - n):
				beginning = timestamps[i]
				ending = timestamps[i + n - 1]
				windows[i] = ending - beginning
				
			print(windows)
			average = np.int64(0)
			minimum = 9223372036854775807
			maximum = -1
			for i in range(len(windows)):
				time = windows[i]
				average += time
				if minimum > time:
					minimum = time
				if maximum < time:
					maximum = time
			average = int(average / len(windows))
				
			results[ind] = (n, average, minimum, maximum)
			print("Average in seconds: ", mu_to_seconds(average))
			
		return results
		
		
	@kernel
	def get_time_to_detect(self, laser_port, apd_port, photon_counts, windows, verbose):
		
		print("Beginning initialization wait analysis")
		
		# Dictionary for recording the initialization times
		results = dict()
		def record(board, start, last):

				# Turn of the laser
				delay(50*us)
				board.ttls[laser_port].off()

				results[n] = last - start
				if verbose: print("Time to detect photons (in mu): ", last - start)
		
		for n in photon_counts:
		
			if verbose: print("Beginning test to detect ", n , " photons")
			
			# Calculate threshold window before dealing with the timeline
			window = windows[n]
		
			# Reset the board and timeline, delaying to avoid RTIOUnderflow Errors
			self.board.reset()
			self.board.get_core().break_realtime()
			delay(1*s) # Change this as needed
			
			start = now_mu()
			if verbose: print("Starting 532 nm pulse at time ", start)
			self.board.ttls[laser_port].on();
			
			if verbose: print("APD beginning to listen at time ", start)
			self.board.register_rising(apd_port, record, start, window, threshold=n)
			
		return results