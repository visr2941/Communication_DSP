# File: pcmfun.py
# Functions for conversion between m(t) and PCM representation 
# Concept: The program takes the "value" from mt (one by one) and divide it by the quantization
# interval length to get the "interval number" in which the "value" belongs. And the code is assigned
# based on the interval number with zero padded in before the code if value is greater than zero or
# 1 if it's smaller than zero. The function mt2pcm is returning the new quantized mt and the code array for the same.

from pylab import *
import numpy as np

def mt2pcm(mt, bits=3):
    """
    Message signal m(t) to binary PCM conversion
    >>> dn = mt2pcm(mt,bits) <<<<
    where mt	normalised (A+1) "analog" message signal
        bits	number of bits used per sample
        dn	binary output sequence in sign-magnitude
            form, MSB (first)
    """
    
    qlevel = np.power(2,bits)   # number of quantization level
    bits=bits-1      # number of bits is reduced by one to incorporate the sign of number
   
    if abs(min(mt)) > abs(max(mt)):     # defining the delta in uniform fashion
        delta = 2*abs(min(mt))/qlevel
    else:
        delta = 2*abs(max(mt))/qlevel

    pow = np.power(2.0,1+arange(-bits,0))    # making array of increasing negative power of 2
    code_array = array([])        # initialisation of code_array
    mt_new_quantized = array([])
    for val in mt:              # starting the loop to check each values in mt
        if val > 0:
            x = floor(val/delta)
            if x == val/delta:     # if val is equal maximum quantization level, it's reduced by 1 to encode it
                x = x-1
            mt_new_quantized = np.append(mt_new_quantized,array([x*delta+0.5*delta]))   # making of new quantized mt
            x_bin = array(mod(floor(outer(array([x]),pow)),2),int)
            code_array = np.append(code_array,hstack((array([[0]]),x_bin)))  # making of code array
        elif val < 0:
            x = floor(abs(val)/delta)
            if x == abs(val)/delta:       # if val is equal maximum quantization level, it's reduced by 1 to encode it
                x = x-1
            mt_new_quantized = np.append(mt_new_quantized,array([-x*delta-0.5*delta]))     ## making of new quantized mt
            x_bin = array(mod(floor(outer(array([x]),pow)),2),int)
            code_array = np.append(code_array,hstack((array([[1]]),x_bin)))  # making of code array
        else:
            mt_new_quantized = np.append(mt_new_quantized,array([0]))     ## making of new quantized mt
            x_bin = array(mod(floor(outer(array([0]),pow)),2),int)
            code_array = np.append(code_array,hstack((array([[0]]),x_bin)))  # making of code array
            
    return  mt_new_quantized, array(code_array,int8)
            
    
    
# Same concept is applied here but in reverse way as applied in mt2pcm 
    
def pcm2mt(dn, bits=3):
    """
    Binary PCM to message signal m(t) conversion
    >>>>> mt = pcm2mt(dn, bits) <<<<<
    where   dn binary output sequence in sign-magnitude form, MSB (sign) first
            bits   number of bits used per sample
            mt  normalized (A=1) "analog" message signal
    """

    dn = array(dn,int)
    mt=array([])
    delta = 2/np.power(2,bits)
    bits=bits-1
    pow = np.power(2.0,arange(bits,0,-1)-1)    # making array of increasing power of 2
    for n in arange(0,int(len(dn)/(bits+1))):
        intvl_number = inner(dn[n*(bits+1)+1:(n+1)*(bits+1)],pow)    # this is the same the interval used in the mt2pcm
        if dn[n*(bits+1)] == 0:
            if intvl_number == np.power(2,bits):
                intvl_number = intvl_number - 1
            mt = np.append(mt, array([intvl_number*delta + 0.5*delta]))   # making the quantized signal
        else:
            if intvl_number == np.power(2,bits):
                intvl_number = intvl_number - 1
            mt = np.append(mt, array([-intvl_number*delta - 0.5*delta]))   # making the quantized signal
        
    return mt
