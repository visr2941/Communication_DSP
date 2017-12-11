function [ chan_data,h ] = chan_model( ser_data,nsym,Ncp,area )
if area == 3
    tau = [0 0.25e-6 0.5e-6 0.9e-6 1.1e-6 1.9e-6 2.1e-6 2.5e-6 3e-6];
p = [10^(0.4) 10^(0.8) 1 10^(0.5) 10^(1.6) 10^(1.8) 10^(1.4) 100 10^(2.5)];
chan = rayleighchan(1e-5,1875,tau,p);
h_tap = chan.PathGains;
h = zeros((Ncp*nsym),1);
for k = 1:2
    h(k) = h_tap(k);
end
chan_data = cconv(ser_data,h,nsym*Ncp);
elseif area == 2
    tau = [0 0.25e-6 0.5e-6 0.75e-6 1e-6 1.25e-6 2e-6 2.5e-6 3e-6];
p = [10^(0.2) 1 10^(0.3) 10^(0.4) 10^(0.2) 1 10^(0.3) 10^(0.5) 10];
chan = rayleighchan(1e-5,625,tau,p);
h_tap = chan.PathGains;
h = zeros(68*nsym,1);
for k = 1:9
    h(k) = h_tap(k);
end
chan_data = cconv(ser_data,h,nsym*68);
else 
    tau = [0 0.25e-6 0.5e-6 0.9e-6 1.1e-6 1.9e-6 2.1e-6 2.5e-6 3e-6];
p = [10 10^(0.4) 10^(0.2) 10^(0.3) 10^(0.4) 10^(0.5) 10^(0.2) 10^(0.8) 10^(0.5)];
chan = rayleighchan(1e-5,625,tau,p);
h_tap = chan.PathGains;
h = zeros(68*nsym,1);
for k = 1:2
    h(k) = h_tap(k);
end
chan_data = cconv(ser_data,h,nsym*68);
end
end

