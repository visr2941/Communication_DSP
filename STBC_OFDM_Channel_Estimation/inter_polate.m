function [ Hest ] = inter_polate( Hp,N,nsym,L,interpol )
if interpol == 1
%linear interpolation
Hls1 = zeros(nsym,N);
k=1;
for i= (1:L+1:N)
    l=0;
    for j = (i:i+L)
        Hls1(:,j) = Hp(:,k) + (l./(L+1))*(Hp(:,k+1)-Hp(:,k));
        l=l+1;
    end
    k = k+1;
end

Hest = Hls1;
elseif interpol == 2;
% second order interpolation
Hls1 = zeros(nsym,N);
Hp1 = [zeros(nsym,1) Hp zeros(nsym,1)];
k=1;
for i= (1:L+1:N)
    l=0;
    for j = (i:i+L)
        a = l/N;
        c1 = a*((a+1)/2);
        c2 = -1*(a-1)*(a+1);
        c3 = a*((a-1)/2);
        Hls1(:,j) = c1*Hp1(:,k) + c2*Hp1(:,k+1) + c3*Hp1(:,k+2); 
        l=l+1;
    end
    k = k+1;
end 
Hest = Hls1;
else
% spline interpolation
Hls1 = zeros(nsym,N);
x = 1:L+1:N;
xx = 1:N;
for i =1:nsym
    Hls1(i,:) = spline(x,Hp(i,:),xx);
end
Hest = Hls1;
end

        


end

