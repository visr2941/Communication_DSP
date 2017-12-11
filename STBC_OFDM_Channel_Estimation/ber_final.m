clear all
close all
clc
area = input('for rural area, enter "1", for urban area, enter "2", for terrain obstructed areas enter "3": ');
estimate = input('for LS estimation, enter "1", for MMSE estimation, enter "2":');
interpol = input('for linear interpolation, enter "1", for polynomial, enter "2", for spline enter "3": ');
defaults = input ('To use default parameters, enter "1", otherwise enter "0": ');
if defaults == 1
    nsym = 10^4;% total no. of OFDM symbols used for simulation
    len_fft = 64;% fft size
    N = 64;% total no. of subcarriers
    cp = 4;% cyclic prefix length
    Ncp = N+cp;% total symbol length including cyclic prefix
    Np = 8;% total no. of pilot tones
    L = (N/Np)-1;% no. of data carriers b/w the pilots
else
    nsym = input('Number of Symbols for simulation =');
    N = input('Number of Carrier =');
    len_fft = input('IFFT bin length =');
    cp = input('cyclic prefix length =');
    Np = input('Number of pilot tones =');
    Ncp = N+cp;% total symbol length including cyclic prefix
    L = (N/Np)-1;% no. of data carriers b/w the pilots
end
%%%% Performance of different OFDM modulation techniques for gaussian channel%%%%

for modlevel = [4 2 1]
    nbitpersym  = (N-Np)*modlevel;   % number of bits per qam OFDM symbol (same as the number of subcarriers for 16-qam)
    nbits = nbitpersym*nsym;
    nmod = (nbitpersym/modlevel); % length of modulated data per symbol
    EbNo        = 0:2:30;
    EsNo= EbNo+10*log10(4);
    snr = EsNo;
    
    %%%%% Transmitter side
    % Random data generation
    t_data=randint(nbits,1,2);
    
    % Data modulation
    mod_data =  mod_sym(t_data,nbits,modlevel);
    
    % Serial to parallel conversion
    par_data = reshape(mod_data,nmod,nsym).';
    
    % pilot insertion
    pilot = 1;
    pilot_data = zeros(nsym,1);
    for i = 1:nsym
        pilot_data(i) = pilot;
    end
    pilot_ins_data = zeros(nsym,64);
    k = 1;
    for i = 1:7:56;
        pilot_ins_data(:,[k:k+7])=[pilot_data(:,1) par_data(:,[i:i+6])] ;
        k = k+8;
    end
    
    % Inverse fourier transform  to obtain the Time doamain data
    IFFT_data =ifft(fftshift(pilot_ins_data.')).';
    a=max(max(abs(IFFT_data)));
    IFFT_data=IFFT_data./a;% Normalization
    
    % Cyclic prefix addition
    cylic_add_data = [IFFT_data(:,[61:64]) IFFT_data].';
    
    % parallel to serial coversion
    ser_data = reshape(cylic_add_data,68*nsym,1);
    
    % Passing through channel
    chan_data = chan_model( ser_data,nsym,Ncp,area );
    
    no_of_error=[];
    ratio=[];
    for ii=1:length(snr)
    % Additive White Gaussian Noise addition
    chan_awgn = awgn(chan_data,snr(ii),'measured'); 
    noise = chan_awgn - chan_data;
    variance = var(noise);
    % serial to parallel coversion
    ser_to_para = reshape(chan_awgn,68,nsym).'; 
    
    %%%% Reciever side
    %cyclic prefix removal
    cyclic_pre_rem = ser_to_para(:,[5:68]);   

    % Fourier transform to obtain freq domain data
    FFT_recdata =a*fftshift(fft(cyclic_pre_rem.')).'; 
    
    % Channel estimation
    Hp = channel_estimation( FFT_recdata,N,nsym,Np,L,estimate, variance);
    
    %interpolation
    Hest  = inter_polate( Hp,N,nsym,L,interpol);
   
    % estimated output
    Y = FFT_recdata;
    X1 = zeros(nsym,N);
    for i = 1:nsym
    h11 = diag(Hest(i,:));
    X1(i,:) = (inv(h11)*(Y(i,:)).');
    end
    
    %pilot removal
    k = 1;
    for i = 1:8:64
    rem_pilot(:,[k:k+6]) = X1(:,[i+1:i+7]); 
    k = k+7;
    end
    
    % Parralel to serial coversion
    ser_data_1 =sqrt(10)* reshape(rem_pilot.',nmod*nsym,1);
    
    figure;
    scatterplot(ser_data_1);
    
    % Demodulation of recieved frequency domain data
    [demod_Data,data2] = demod_sym(ser_data_1,nbits,modlevel);
    
    % error rate calculation
    [no_of_error(ii),ratio(ii)]=biterr(t_data , data2) ; 
    ratio(ii);
    end
    colors = ['r' 'b' 'm' 'k'];
    semilogy(EbNo,ratio,colors(modlevel),'linewidth',2);
    hold on;
end
axis([0 15 10^-5 1])
legend('16 QAM','QPSK','BPSK')
grid on
xlabel('EbNo');
ylabel('BER');
title('Bit error probability curve for different modulations using OFDM');
    
    
    
    
    
    
    
    