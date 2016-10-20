#!/usr/bin/python

import scipy.signal
import numpy
import math
from util import *

FILTER_INDEX=0
SIGNAL_COMBINER_INDEX=1

def get_freq_amplitudes(input_signal, sampling_freq):
    # Returns a dict where the key is the frequency and the value is the amplitude of all the input signal's composite sinusoids 
    num_samples = len(input_signal)
    freq_res = float(sampling_freq) / num_samples
    nyquist_limit = sampling_freq/2.0 
    discrete_nyquist_cutoff = int(math.floor(nyquist_limit/freq_res))
    FFT = numpy.fft.fft(input_signal)
    two_sided_magnitudes = numpy.absolute(FFT)
    one_sided_magnitudes = 2.0*two_sided_magnitudes[:discrete_nyquist_cutoff+1]
    averaged_one_sided_magnitudes = one_sided_magnitudes/float(num_samples)
    ans = dict(zip([freq_res*i for i in xrange(num_samples)], averaged_one_sided_magnitudes))
    return ans

class Filter(object):
    
    def __init__(self, a0=list(), b0=list()): 
        self.a = numpy.array(a0, dtype=numpy.float64) # IIR Filter Coefficients
        self.b = numpy.array(b0, dtype=numpy.float64) # FIR Filter Coefficients
    
    def __init__(self, filter0): 
        self.a = numpy.array(filter0.a)
        self.b = numpy.array(filter0.b)
    
    def apply(self, input_signal):
        output_signal = scipy.signal.lfilter(self.b, self.a, input_signal, axis=0)
        return output_signal
    
class SignalCombiner(object):
    
    def __init__(self, list_of_weights0): 
        self.list_of_weights=numpy.array(list_of_weights0, dtype=numpy.float64)

    def apply(self, list_of_input_signals): 
        output_signal = numpy.sum([weight*input_signal for input_signal, weight in zip(list_of_input_signals,self.list_of_weights)], axis=0)
        return output_signal

class FilterNetwork(object):
    
    def __init__(self, num_layers=3, num_units_per_layer=3, num_fir_coefficients=10000, num_iir_coefficients=10000): 
        # To access a filter unit, we use self.network[layer_index, unit_index]
        self.network = \
                        [
                            [
                                (
                                    Filter([random.uniform(-1.0,1.0) for i in xrange(num_fir_coefficients)],[random.uniform(-1.0,1.0) for i in xrange(num_iir_coefficients)]), 
                                    None if layer_index==0 else SignalCombiner([random.uniform(0.0,1.0) for i in xrange(num_units_per_layer)])
                                )
                                for unit_index in xrange(num_units_per_layer)
                            ] 
                            for layer_index in xrange(num_layers)
                        ]
        self.final_combiner = SignalCombiner([random.uniform(0,1) for i in xrange(num_units_per_layer)])
    
    def get_num_layers(self):
        return len(self.network)
    
    def get_num_units_per_layer(self):
        return len(self.network[0])
    
    def apply(self, input_signal): 
        output_signals_network = [([None]*self.get_num_units_per_layer()) for layer_index in xrange(self.get_num_layers())]
        for layer_index, layer in enumerate(self.network):
            for unit_index, unit in enumerate(layer):
                if layer_index == 0:
                    current_input_signal = input_signal
                else:
                    current_input_signal = unit[SIGNAL_COMBINER_INDEX].apply(output_signals_network[layer_index-1])
                output_signals_network[layer_index][unit_index] = unit[FILTER_INDEX].apply(current_input_signal)
        return self.final_combiner.apply(output_signals_network[-1])
    
#class FilterNetworkGeneticAlgorithm(object):
#    
#    def __init__(self, population_size0=10, num_generations0=10, elite_percent0=0.8): 
#        self.population_size = population_size0
#        self.num_generations = num_generations0
#        self.elite_percent = elite_percent0
#        self.population = [FilterNetwork() for i in xrange(population_size)]
#    
#    def run_generation(self, num_generations_to_run=1):
#        for generation_index in xrange(num_generations_to_run):
#            # FIR Mutations
#            # IIR Mutations
#            # Combiner Mutations
#            # Cross Over

