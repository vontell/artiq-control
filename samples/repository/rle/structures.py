# A collection of utility classes useful for
# ARTIQ experiment

from artiq.experiment import kernel

# A class which replaces arrays for use with ARTIQ's python. Includes functions
# for appending, getting, setting, and popping. Currently only supports 
# integers
# Written by Aaron Vontell on January 17, 2017
class PreAllocArray:
	
	@kernel
	def __init__(self, size):
		'''Creates a newly allocated array with the given size'''
		
		self.array = [0 for i in range(size)]
		self.head = 0
		
	@kernel
	def append(self, value):
		'''Append `value` to the head of the list'''
		
		self.array[self.head] = value
		self.head = self.head + 1