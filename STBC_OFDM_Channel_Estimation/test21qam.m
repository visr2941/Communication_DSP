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
b2=round(rand()*15);
s2=modulate(hm,b2);
h=rey(2,1);
h1=h(1,1);
h2=h(2,1);
sig=sqrt(0.5/(10^(snr/10)));                                 
n=sig*(randn(1,2)+1j*randn(1,2)); 
r1=h1*s1+h2*s2+n(1,1);
r2=-h1*conj(s2)+h2*conj(s1)+n(1,2);

%decoding s1
chk=hm.constellation;
for i=1:1:length(chk)
    t=abs((r1*conj(h1)+conj(r2)*h2-chk(1,i)))^2+((abs(h1))^2+(abs(h2))^2-1)*(abs(chk(1,i)))^2;
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
%decoding s2
for i=1:1:16
    t=abs((r1*conj(h2)-conj(r2)*h1-chk(1,i)))^2+((abs(h1))^2+(abs(h2))^2-1)*(abs(chk(1,i)))^2;
    if i==1
        th=t;
        d2=chk(1,i);
    else
        if t<th
            th=t;
            d2=chk(1,i);
        end
    end
end
ds1=demodulate(hd,d1);
ts1=demodulate(hd,s1);
ds2=demodulate(hd,d2);
ts2=demodulate(hd,s2);
biterrorin2symbol=sum(xor(ds1,ts1))+sum(xor(ds2,ts2));
total=total+biterrorin2symbol;
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







    







    
    
    
