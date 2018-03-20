from pylab import *
import ascfun as af
import wavfun as wf
filename = input("Enter the file name (wav): ")
rt, fs = wf.wavread(filename)
bits = 8
#n = int(floor(len(rt)/float(fs)/tb)) 	

dn=[]
#comp_val = (max(rt) + min(rt))/2.0   # to decide whether the bit is 1 or zero

# making a list of all bits
for j in rt:
	if j > 0:
		dn = dn + [1]
	else:
		dn = dn + [0]

# counding the continuous 1s or 0s
k=dn[0] 
n=0  # track the count
lst=[]  # this list will contain the count of continuous 1s or 0s
for i in dn:
	if k == i:
		n=n+1
		continue
	else:
		k=i
		lst = lst + [n]
		n=0

# getting the minimum value of the list and printing it
print("The bit rate is below ")
print(fs/min(lst))

