# File: sine100.py
# Ask for sampling frequency fs and then generates and plots
# differential and integral value of sine wave and rectangular wave.

#/usr/bin/python3

from pylab import *

#fs = float(input("Enter the sampling frequency: "))
fm = 100  			# frequency of the signal
tlen = 0.05  			# time for 5 period of the signal

t = arange(0,round(tlen*fs))/float(fs) 		# defining the range of time
st = sin(2*pi*fm*t)  		# sinewave
rt = sign(st)

rdt = diff(hstack((0,rt)))*fs 	# finding the value of slope of rt at t
rdit = cumsum(rdt)/fs 	# finding the original rt from rdt


plot()
plot(t,rdt,'-r*')
xlabel('time (s) ---->')
ylabel('rdt ----->')
title('Differentiation of rt "rectangular wave", Sampling Frequency = %s Hz' %fs)
show()

plot()
plot(t,rdit,'-b*')
xlabel('time (s) ---->')
ylabel('rdit ----->')
title('Integration of rdt, to recover the rt "rectangular wave", Sampling Frequency = %s Hz' %fs)
ylim([-1.5,1.5])
show()

sdt = diff(hstack((0,st)))*fs     # finding the value of slope of st at t
sdit = cumsum(sdt)/fs   # finding the original st from sdt


plot() 
plot(t,sdt,'-r*')
xlabel('time (s) ---->')
ylabel('sdt ----->')
title('Differentiation of st "sine wave", Sampling Frequency = %s Hz' %fs)
show()


plot()
plot(t,sdit,'-b*')
xlabel('time (s) ---->')
ylabel('sdit ----->')
title('Integration of sdt, to recover the st "sine wave", Sampling Frequency = %s Hz' %fs)
show()

