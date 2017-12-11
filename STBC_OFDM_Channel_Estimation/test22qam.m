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
h=rey(2,2);
h11=h(1,1);
h21=h(2,1);
h12=h(1,2);
h22=h(2,2);
sig=sqrt(0.5/(10^(snr/10)));                                 
n=sig*(randn(2,2)+1j*randn(2,2)); 
%r(time slot)(rx antenna)
r11=h11*s1+h21*s2+n(1,1);
r12=h12*s1+h22*s2+n(2,1);
r21=-h11*conj(s2)+h21*conj(s1)+n(1,2);
r22=-h12*conj(s2)+h22*conj(s1)+n(2,2);

%decoding s1 and s2
chk=hm.constellation;
for i=1:1:length(chk)
    for l=1:1:length(chk)
        t=(abs(r11-h11*chk(1,i)-h21*chk(1,l)))^2+(abs(r12-h12*chk(1,i)-h22*chk(1,l)))^2+(abs(r21-(-h11*conj(chk(1,l))+h21*conj(chk(1,i)))))^2+(abs(r22-(-h12*conj(chk(1,l))+h22*conj(chk(1,i)))))^2;
        if i==1 && l==1
            th=t;
            d1=chk(1,i);
            d2=chk(1,l);
        else
            if t<th
                th=t;
                d1=chk(1,i);
                d2=chk(1,l);
            end
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







    







    
    
    
