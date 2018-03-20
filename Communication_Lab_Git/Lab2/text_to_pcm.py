# This program will accpet the text string and convert
# it into flat top PAM s(t) signal.

from pylab import *
from ascfun import *
import wavfun as wf

txt = input("Enter the text: ")
fs = 44100
fb = 100
tb = 1/float(fb)

dn = asc2bin(txt)   # as2bin will change the txt to stream of bits
n=len(dn) 	# length of dn sequence
ixl = round(-0.5*tb*fs) 	# the starting left index of the st
ixr = round((n-0.5)*fs*tb)	# the right most index of the st
tt = arange(ixl,ixr)/float(fs)  # time axis for st


# making differtial of the sequence and the integrating it

dnt = diff(hstack((0,dn)))*fs    # taking differential of dn

ddnt=[]
for i in dnt:       # adding zeros in between two dn bits 
	ddnt = ddnt + [i] + list(zeros(round(tb*fs)-1)) 


ddnt_prime = array(ddnt)   	# changing list into numpy array
st = cumsum(ddnt_prime)/float(fs)      # integrating the differential of st to get st

# Plotting the st

subplot(211)
plot(tt, st, linewidth=4)
grid()
xlabel('time ---->')
ylabel('st ---->')
title('Corresponding PAM signal of input text characteri "%s" (Method1)' %txt)
ylim((-0.2,1.2))

# creating Wavefile
wf.wavwrite(0.999*st/float(max(abs(st))),fs,'MyTest.wav')

###############################################################################################################################

# Below is an alternative way of making PAM signal
# here we will just repeat the number of ones or zeros
# as number of times as number of samples in one pulse

dnn = [repeat(c,round(fs*tb)) for c in dn]    # repeating the one or zero as many samples are there in one pulse
st=[]
for i in dnn:                  # making of st signal
	st = st + list(i)

subplot(212)
plot(tt, st, linewidth=4)
ylim((-0.2,1.2))
grid()
xlabel('time ---->')
ylabel('st ---->')
title('Corresponding PAM signal of input text character "%s" (Method2)' %txt)

show()
