# Configurable tests and experiments for Rabi oscillations
# in Nitrogen Vacancy Centers. 

from artiq.experiment import Experiment, kernel, us

class RabiExperiment:
  
	def __init__(self, board):
		
		self.board = board
		
	@kernel
	def get_photon_windows(self, laser_port, apd_port, photon_counts, timeout_fn, verbose):
		
		print("Beginning initialization window analysis")
		
		# Dictionary for recording the window times
		results = {}
		
		
	@kernel
	def get_time_to_detect(self, laser_port, apd_port, photon_counts, windows, verbose):
		
		print("Beginning initialization wait analysis")
		
		# Dictionary for recording the initialization times
		results = {}
		def record(board, start, last):

				# Turn of the laser
				delay(50*us)
				board.ttls[laser_port].off()

				results[n] = last - start
				if verbose: print("Time to detect photons (in mu): ", last-start)
		
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