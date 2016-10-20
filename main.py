#!/usr/bin/python

"""

Data Driven Reverb Simulator

TODO:
    Update usage()
    Get crossover working
    Read http://www.eas.uccs.edu/~mwickert/ece2610/lecture_notes/ece2610_chap8.pdf on how to solve for coefficients

"""

import os
import sys
import pdb
import time
import scipy.io.wavfile
import scipy.signal
import numpy
from util import *
from FilterNetwork import *

START_TIME=time.time()

def convert_hertz(freq, sample_rate=44100.0):
    # convert frequency in hz to units of pi rad/sample
    return freq * 2.0 / sample_rate

def usage(): 
    # Sample Usage: python main.py input.wav ./results -denoising_sigma 2
    print >> sys.stderr, ''
    print >> sys.stderr, 'Usage: python '+__file__+' input_image out_dir <options>'
    print >> sys.stderr, ''
    print >> sys.stderr, 'Sample Usage: python '+__file__+' input.png ./results -denoising_sigma 2'
    print >> sys.stderr, ''
    print >> sys.stderr, 'EXPLANATION TEXT.'
    print >> sys.stderr, ''
    print >> sys.stderr, 'Options:'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -denoising_sigma <float>'
    print >> sys.stderr, '        We first smooth the data with a Gaussian filter. The default value is 2.0.'
    print >> sys.stderr, ''
    exit(1)

def main():
    if len(sys.argv) < 3:
        usage()
    
    # Get Params
    input_wav_location = os.path.abspath(sys.argv[1])
    out_dir = os.path.abspath(sys.argv[2]) # the output directory
    makedirs(out_dir)
    denoising_sigma = float(get_command_line_param_val_default_value(sys.argv,'-denoising_sigma',2))
    
    print "Parameters: "
    print "    Input WAV File Location:",input_wav_location
    print "    Output Directory:",out_dir
    print "    Denoising Sigma:",denoising_sigma
    print 
    
    input_sample_rate, input_samples = scipy.io.wavfile.read(input_wav_location)
    output_wav_location = os.path.join(out_dir,"output.wav")
    
#    fn = FilterNetwork(num_layers=3, num_units_per_layer=3, num_fir_coefficients=3, num_iir_coefficients=3)
#    print fn.network[1][1][0].a
#    fn.mutate_IIR(1,1)
#    print fn.network[1][1][0].a
    
    num_samples = 31
    freq = 1 # full periods per second
    sampling_freq = 8 
    total_time = num_samples/sampling_freq
    total_num_cycles = freq*total_time
    total_num_degrees = total_num_cycles*360.0
    num_degrees_per_sample = total_num_degrees/float(num_samples)
    
    sine_wave = numpy.sin(numpy.array([(num_degrees_per_sample)*i+50 for i in xrange(num_samples)]) * numpy.pi / 180. )
    sine_wave = numpy.concatenate((sine_wave,[0]*(32-len(sine_wave))))
    freq_amps = get_freq_amplitudes(sine_wave, sampling_freq)
    def p(i):
        print i
#        return i
    print [p(e) for e in freq_amps.items() if e[1]>1e-15]
    
#    output_samples = numpy.asarray(filt.apply(input_samples), dtype=numpy.int16)
    
#    scipy.io.wavfile.write(output_wav_location, input_sample_rate, output_samples)
    
    print 
    print 'Total Run Time: '+str(time.time()-START_TIME) 
    print 

if __name__ == '__main__': 
    main() 

