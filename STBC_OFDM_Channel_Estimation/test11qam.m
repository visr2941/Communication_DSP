
clear
clc
iter=1;
hm=modem.qammod(16);
hd=modem.qamdemod(16);
hd.outputtype='bit';
for snr=0:5:30
k=1;
total=0;
while (k<=10000)
b1=round(rand()*15);
s1=modulate(hm,b1);
h=rey(1,1);
h1=h(1,1);
sig=sqrt(0.5/(10^(snr/10)));                                 
n=sig*(randn(1,1)+1j*randn(1,1)); 
r1=h1*s1+n(1,1);


%decoding s1
chk=hm.constellation;
for i=1:1:length(chk)
    t=(abs((r1-h1*chk(1,i))))^2;
    if i==1
        th=t;
        d1=chk(1,i);
    else
        if t<th
            th=t;
            d1=chk(1,i);
        end
    end
end

ds1=demodulate(hd,d1);
ts1=demodulate(hd,s1);

biterrorin1symbol=sum(xor(ds1,ts1));
total=total+biterrorin1symbol;
k=k+1;
end
berate(1,iter)=total;
iter=iter+1;
end
snr=0:5:30;
for i=1:1:length(berate)
    berate(1,i)=berate(1,i)/10000;
end
semilogy(snr,berate)
hold on





    







    
    
    
