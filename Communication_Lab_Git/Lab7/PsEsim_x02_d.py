# Simulation of probability of symbol error Ps(E) for
# data transmission using uncoded PAM
from pylab import *
from numpy import *
from sys import argv
from ccfun import *
EbNodB= argv
import pamfun
# ***** Parameters *****
Fs = 1000                                             # Sampling rate
FB = 100                                              # Baud rate FB
#EbNodB = float(EbNodB[-1])                                            # Specified SNR Eb/No in dB
EbNodB = 2
N = 100000
    
# Number of symbols

ptype, pparms = 'rect',[]                             # Pulse type/parameters
an_set = [-1,+1]                                      # Set of possible an values
M = len(an_set)                                       # Number of signal levels

# ***** Compute Eb for given p(t) and signal constellation *****
Es_prime = 0
for i in an_set:
    tt, pt = pamfun.pam12(array([i]), FB, Fs, ptype, pparms)      # PAM signal
    Es_prime += (cumsum(pt*pt)/Fs)[-1]
Eb = Es_prime

# ***** Generate PAM signal using random data *****

dn = array(floor(2*rand(N)),int)                      # Random binary data signal
eb = ccencod10(dn, array([[1,0],[1,1]]), trim='True')
an = 2*eb-1                                           # Polar binary sequence
tt, st = pamfun.pam12(an, FB, Fs, ptype, pparms)      # PAM signal


# ***** Generate Gaussian noise signal *****
nt = randn(len(tt))                                   # Gaussian noise


# >>>>> Compute An such that rt has desired SNR Eb/No <<<<<

N0 = Eb/(10**(EbNodB/10))
An = pow(N0*Fs/2, 0.5)
rt = st + An*nt                                       # Noisy PAM signal

# ***** PAM signal receiver *****
dly = 0
bn, bt, ixn = pamfun.pamrcvr10(tt, rt, [FB, dly], ptype, pparms)
dnhat = array(zeros(len(bn)),int)
ixp = where(bn > 0)[0]
dnhat[ixp] = ones(len(ixp))                             # Received binary data, quantized
ixn = where(bn <= 0)[0]
dnhat[ixn] = -1*ones(len(ixn))
db, DM = ccdecod10(dnhat)
nerror = list(abs(dn - db)).count(1)