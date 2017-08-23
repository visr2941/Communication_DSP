function [mod_data] = mod_sym(t_data,nbits,modlevel)
if modlevel == 4
M = modem.qammod('M',2^modlevel); % modulation object
qamdata=bi2de(reshape(t_data,modlevel,(nbits/modlevel)).','left-msb');
maping = bin2gray(qamdata,'qam',2^modlevel);
mod_data =1/sqrt(10)* modulate(M,maping);
else
M = modem.pskmod('M',2^modlevel); % modulation object
pskdata=bi2de(reshape(t_data,modlevel,(nbits/modlevel)).','left-msb');
maping = bin2gray(pskdata,'psk',2^modlevel);
mod_data =1/sqrt(10)* modulate(M,maping);
end
end

