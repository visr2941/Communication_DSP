function [demod_Data,data2] = demod_sym(ser_data_1,nbits,modlevel)
if modlevel == 4
z=modem.qamdemod('M',2^modlevel);
demod_Data = demodulate(z,ser_data_1);  %demodulatin the data
demaping = gray2bin(demod_Data,'qam',2^modlevel);
data1 = de2bi(demaping,'left-msb');
data2 = reshape(data1.',nbits,1);
else
z=modem.pskdemod('M',2^modlevel);
demod_Data = demodulate(z,ser_data_1);  %demodulatin the data
demaping = gray2bin(demod_Data,'psk',2^modlevel);
data1 = de2bi(demaping,'left-msb');
data2 = reshape(data1.',nbits,1);
end

end

