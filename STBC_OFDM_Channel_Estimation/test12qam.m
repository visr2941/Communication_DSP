clear
clc
iter=1;

hm=modem.qammod(16);
hd=modem.qamdemod(16);
hd.outputtype='bit';
for snr=0:5:30
k=1;
total=0;
while (k<=20000)
b1=round(rand()*15);
s1=modulate(hm,b1);
h=rey(1,2);
h1=h(1,1);
h2=h(1,2);
sig=sqrt(0.5/(10^(snr/10)));                                 
n=sig*(randn(2,1)+1j*randn(2,1)); 
r1=h1*s1+n(1,1);
r2=h2*s1+n(2,1);
cs=conj(h1)*r1+conj(h2)*r2;
%decoding s1
chk=hm.constellation;
for i=1:1:length(chk)
    %t=(abs(cs-((abs(h1))^2+(abs(h1))^2)*chk(1,i)))^2;
    t=(abs(r1-h1*chk(1,i)))^2+(abs(r2-h2*chk(1,i)))^2;
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
    berate(1,i)=berate(1,i)/20000;
end
semilogy(snr,berate)
hold on


    





    







    
    
    
