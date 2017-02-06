import numpy as np
import matplotlib.pyplot as plt

num_trials = 1000
thresholds = range(1, 21)
max_threshold = max(thresholds)
fidelity = [0] * max_threshold

photon_stream_lambda = 10 ** -6
background_lambda = 10 ** -2
start_delay_lambda = 10 ** -6

for i in range(num_trials):
	fake_pulse = np.random.exponential(photon_stream_lambda, max_threshold)
	
	for i in range(1, len(fake_pulse)):
		fake_pulse[i] = fake_pulse[i] + fake_pulse[i - 1]
	
	background = np.random.exponential(background_lambda, max_threshold)
	start_delay = np.random.exponential(start_delay_lambda)
	
	invalid = [i for i in fake_pulse if i < start_delay] + [i for i in background if i < start_delay]
		
	bad_n = len(invalid)
	for i in range(bad_n + 1, max_threshold):
		fidelity[i] = fidelity[i] + 1

for i in range(len(fidelity)):
	fidelity[i] = (fidelity[i] / num_trials) * 100
		
plt.plot(thresholds, fidelity)
plt.title("Simulated Initialization Fidelity")
plt.xticks(thresholds)
plt.xlabel("Threshold (photons)")
plt.ylabel("Fidelity (%)")
plt.show()