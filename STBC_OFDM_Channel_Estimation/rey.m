function H=rey(Nt,Nr)

H=zeros(Nt,Nr);
R=eye(Nt*Nr);                                               %Correlation matrix. 
X=randn(Nt*Nr,1)/sqrt(2)+j*randn(Nt*Nr,1)/sqrt(2);          %Channel coefficients
H=reshape(R'*X,Nt,Nr);                                      %The matrix.




