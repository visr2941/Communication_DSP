function [ Hp ] = channel_estimation( FFT_recdata,N,nsym,Np,L,estimate,variance)
if estimate == 1
Y = FFT_recdata;
% pilot extraction
Yp = zeros(nsym,Np);
k = 1;
for i = 1:(L+1):N
    Yp(:,k) = Y(:,i);
    k= k+1;
end
Xp = zeros(Np,Np);
for i = 1:Np
    Xp(i,i) = 1;
end
Hpls = zeros(nsym,Np);
for i = 1:nsym
Hpls(i,:) = (inv(Xp)*(Yp(i,:).')).';
end
Hpls(:,(Np+1)) = zeros(nsym,1);
Hp = Hpls;

else
    Y = FFT_recdata;
% pilot extraction
Yp = zeros(nsym,Np);
k = 1;
for i = 1:L+1:N
    Yp(:,k) = Y(:,i);
    k= k+1;
end
Xp = zeros(Np,Np);
for i = 1:Np
    Xp(i,i) = 1;
end
Hpls = zeros(nsym,Np);
for i = 1:nsym
Hpls(i,:) = (inv(Xp)*(Yp(i,:).')).';
end

Hpmmse = zeros(nsym,Np);
for i = 1:nsym
    hh=diag(Hpls(i,:));
    hh_myu = sum(hh, 1)/Np;                    
    hh_mid = hh - hh_myu(ones(Np,1),:);        
    sum_hh_mid= sum(hh_mid, 1);
    Rhh = (hh_mid' * hh_mid- (sum_hh_mid'  * sum_hh_mid) / Np) / (Np - 1);
    Hpmmse(i,:) = (Rhh*inv(Rhh + variance*inv(Xp*Xp'))*Hpls(i,:).').';
end

Hp = Hpmmse; 
end
end

