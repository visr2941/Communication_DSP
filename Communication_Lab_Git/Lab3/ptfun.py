# File: pamfun.py
# Functions for pulse amplitude modulation (PAM)
from numpy import *
def pampt(sps, ptype, pparms=[]):

    # ***** Set up PAM pulse p(t) *****
    ptype = ptype.lower()    # Convert ptype to lowercase
    
    # Set left/right limits for p(t)
    if (ptype=='rect' or ptype == 'man'):
        kL = -0.5; kR = -kL
    else:
        kL = -1.0; kR = -kL
    
    # Default left/right limits
    ixpL = ceil(sps*kL)        # Left index for p(t) time axis
    ixpR = ceil(sps*kR)        # Right index for p(t) time axis
    ttp = arange(ixpL,ixpR)            # Time axis for p(t)
    pt = zeros(len(ttp))        # Initialize pulse p(t)
    #sps = max(ttp)
    if (ptype=='rect'):        # Rectangular p(t)
        pt = ones(len(ttp))
    elif (ptype == 'tri'):
        pt = array([(1+i/sps) if i/sps+1 < 1.0 else (1-i/sps) for i in list(ttp)])
    elif (ptype=='sinc'):
        k=pparms[0]
        kL = -1.0*k; kR = -kL
        ixpL = ceil(sps*kL)        # Left index for p(t) time axis
        ixpR = ceil(sps*kR)        # Right index for p(t) time axis
        ttp = arange(ixpL,ixpR)     # Time axis for p(t)
        pt = zeros(len(ttp))
        beta=pparms[1]
        pt = array([sin(pi*t/sps)/(pi*t/sps) if t!= 0  else  1.0 for t in list(ttp)])
        pt=pt*kaiser(len(pt), beta)
    elif (ptype=='man'):
        pt = hstack((ones(int(len(pt)/2))-2, ones(len(pt)-int(len(pt)/2))))
    elif (ptype=='rcf'):
        k=pparms[0]
        alpha=pparms[1]
        kL = kL*k; kR = -kL
        ixpL = ceil(sps*kL)        # Left index for p(t) time axis
        ixpR = ceil(sps*kR)        # Right index for p(t) time axis
        ttp = arange(ixpL,ixpR)            # Time axis for p(t)
        pt = zeros(len(ttp))
        ix0 = where(ttp==0)[0]
        pt[ix0] = array([1.0])
        ix0 = where(ttp==sps/(2*alpha))[0]
        pt[ix0] = array([0])
        ix0 = where(ttp==-sps/(2*alpha))[0]
        pt[ix0] = array([0])
        ix_rest = where(logical_and(logical_and(ttp!=0, ttp != sps/(2*alpha)), ttp != -sps/(2*alpha) ))[0]
        ttp = ttp[ix_rest]
        pt[ix_rest] = (sin(pi*ttp/sps)/(pi*ttp/sps))*(cos(pi*alpha*ttp/sps)/(1-power(2*alpha*ttp/sps,2)))
    elif ptype=='rrcf':
        k=pparms[0]
        alpha=pparms[1]
        kL = kL*k; kR = -kL
        ixpL = ceil(sps*kL)		# Left index for p(t) time axis
        ixpR = ceil(sps*kR)		# Right index for p(t) time axis
        ttp = arange(ixpL,ixpR)  	 # Time axis for p(t)
        pt = zeros(len(ttp))
        ix0= where(ttp==0)[0]
        pt[ix0] = 1 - alpha +(4*alpha/pi)
        ix0 = where(logical_or(ttp== -sps/(4*alpha), ttp==sps/(4*alpha)))[0]
        pt[ix0] = (alpha/2**0.5)*(((1+2/pi)*sin(pi/(4*alpha))) + ((1-2/pi)*cos(pi/(4*alpha))))
        ix0 = where(logical_and(logical_and(ttp != 0, ttp != sps/(4*alpha)),ttp != -sps/(4*alpha)))[0]
        t=ttp[ix0]
        p = pi*t/sps
        a = alpha*t/sps
        pt[ix0]= sps*(sin((1-alpha)*p) + 4*a*cos((1+alpha)*p))/(pi*t*(1-(4*a)**2))
    else:
        print("ptype '%s' is not recognized" % ptype)
    
    # ***** Filter with h(t) = p(t) *****
    return pt





def pamhRt(sps, ptype, pparms=[]):

    # ***** Set up PAM pulse p(t) *****
    ptype = ptype.lower()    # Convert ptype to lowercase
    
    # Set left/right limits for p(t)
    if (ptype=='rect' or ptype == 'man'):
        kL = -0.5; kR = -kL
    else:
        kL = -1.0; kR = -kL
    
    # Default left/right limits
    ixpL = ceil(sps*kL)        # Left index for p(t) time axis
    ixpR = ceil(sps*kR)        # Right index for p(t) time axis
    ttp = arange(ixpL,ixpR)            # Time axis for p(t)
    pt = zeros(len(ttp))        # Initialize pulse p(t)
    #sps = max(ttp)
    if (ptype=='rect'):        # Rectangular p(t)
        pt = ones(len(ttp))
    elif (ptype == 'tri'):
        pt = array([(1+i/sps) if i/sps+1 < 1.0 else (1-i/sps) for i in list(ttp)])
    elif (ptype=='sinc'):
        k=pparms[0]
        kL = -1.0*k; kR = -kL
        ixpL = ceil(sps*kL)        # Left index for p(t) time axis
        ixpR = ceil(sps*kR)        # Right index for p(t) time axis
        ttp = arange(ixpL,ixpR)     # Time axis for p(t)
        pt = zeros(len(ttp))
        beta=pparms[1]
        pt = array([sin(pi*t/sps)/(pi*t/sps) if t!= 0  else  1.0 for t in list(ttp)])
        pt=pt*kaiser(len(pt), beta)
    elif (ptype=='man'):
        pt = hstack((ones(int(len(pt)/2))-2, ones(len(pt)-int(len(pt)/2))))
    elif (ptype=='rcf'):
        k=pparms[0]
        alpha=pparms[1]
        kL = kL*k; kR = -kL
        ixpL = ceil(sps*kL)        # Left index for p(t) time axis
        ixpR = ceil(sps*kR)        # Right index for p(t) time axis
        ttp = arange(ixpL,ixpR)            # Time axis for p(t)
        pt = zeros(len(ttp))
        ix0 = where(ttp==0)[0]
        pt[ix0] = array([1.0])
        ix0 = where(ttp==sps/(2*alpha))[0]
        pt[ix0] = array([0])
        ix0 = where(ttp==-sps/(2*alpha))[0]
        pt[ix0] = array([0])
        ix_rest = where(logical_and(logical_and(ttp!=0, ttp != sps/(2*alpha)), ttp != -sps/(2*alpha) ))[0]
        ttp = ttp[ix_rest]
        pt[ix_rest] = (sin(pi*ttp/sps)/(pi*ttp/sps))*(cos(pi*alpha*ttp/sps)/(1-power(2*alpha*ttp/sps,2)))
    elif ptype=='rrcf':
        k=pparms[0]
        alpha=pparms[1]
        kL = kL*k; kR = -kL
        ixpL = ceil(sps*kL)		# Left index for p(t) time axis
        ixpR = ceil(sps*kR)		# Right index for p(t) time axis
        ttp = arange(ixpL,ixpR)  	 # Time axis for p(t)
        pt = zeros(len(ttp))
        ix0= where(ttp==0)[0]
        pt[ix0] = 1 - alpha +(4*alpha/pi)
        ix0 = where(logical_or(ttp== -sps/(4*alpha), ttp==sps/(4*alpha)))[0]
        pt[ix0] = (alpha/2**0.5)*(((1+2/pi)*sin(pi/(4*alpha))) + ((1-2/pi)*cos(pi/(4*alpha))))
        ix0 = where(logical_and(logical_and(ttp != 0, ttp != sps/(4*alpha)),ttp != -sps/(4*alpha)))[0]
        t=ttp[ix0]
        p = pi*t/sps
        a = alpha*t/sps
        pt[ix0]= sps*(sin((1-alpha)*p) + 4*a*cos((1+alpha)*p))/(pi*t*(1-(4*a)**2))
    else:
        print("ptype '%s' is not recognized" % ptype)

    hRt = pt[::-1]                                              # h_R(t) = p(-t)
    hRt = 1/sum(power(pt,2.0))*hRt                              # h_R(t) normalized

    return hRt
    
