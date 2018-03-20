# %load to_find_bit_rate.py
from pylab import *
import ascfun as af
import wavfun as wf
###filename = input("Enter the file name (wav): ")
rt, fs = wf.wavread("ftpam_sig02.wav")
bits = 8
#n = int(floor(len(rt)/float(fs)/tb)) 	

dn=[]
comp_val = (max(rt) + min(rt))/2.0
for j in rt:
	if j > comp_val:
		dn = dn + [1]
	else:
		dn = dn + [0]


k=dn[0]
n=0
lst=[]

# This will count consecutive zeros or ones in the bit stream sequence of file
# and the bit rate will be fs divided by the minimum of this count

for i in dn:
	if k == i:
		n=n+1
		continue
	else:
		k=i
		lst = lst + [n]
		n=0


print("The approx. bit rate is below ")
print(fs/min(lst))