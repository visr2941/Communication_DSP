#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>


using namespace std;

#define pi M_PI

template <typename T=int>
class Complex {
    T real, imag;
public:
    Complex() {real = 0; imag = 0;}
    Complex(T x, T y): real(x), imag(y) {}
    //Complex(T x, T y): real(x), imag(y) {}
    
    Complex operator+(Complex const & z2) 
    {
        Complex z; 
        z.real = real + z2.real;
        z.imag = imag + z2.imag;
        return z;
    }
    
    Complex operator*(Complex const & z2) 
    {
        Complex z; 
        z.real = real*z2.real - imag*z2.imag;
        z.imag = real*z2.imag + z2.real*imag;
        return z;
    }
    
    Complex operator-(Complex const & z2) 
    {
        Complex z; 
        z.real = real - z2.real;
        z.imag = imag - z2.imag;
        return z;
    }
    
    void operator()(T x, T y) 
    {
        real = x;
        imag = y;
    }
    
    void polar_complex(double angle)
    {
        real = cos(angle);
        imag = sin(angle);
        //cout << "angle " << angle << " " << real <<  " " << imag << endl;
    }
    
    template <typename U>
    friend ostream & operator<<(ostream & op, Complex<U> & z);
    
    friend vector<Complex<double>> nthroot(int N);
    
    //ostream & operator<<() {cout << real << " + " << imag << endl; } // if we define it here, to call operator <<, we will need to call it as z<<(cout);
    
};

template <typename U>
ostream & operator<<(ostream & op, Complex<U> & z) 
{
    op << z.real << setprecision(8) << fixed; 
    if(z.imag>=0)
        op << " + j" << setprecision(8) << fixed << abs(z.imag) <<  endl;
    else
        op << " - j" << setprecision(8) << fixed << abs(z.imag) << endl;
    
    return op; 
}

/*
template <typename T=Complex<double> >
vector<T> fft(vector<T> sig, int N)
{
    vector<Complex<double> > sig_fft(N);
    Complex<double> wn, temp1, temp2, temp3;
    
    for (int k = 0; k < N; k++)
    {
        for (int i = 0; i < N/2; i++)
        {
            wn.polar_complex((double) (-2)*pi*k*i/N);
            temp1 = wn;
            wn.polar_complex((double) (-2)*pi*0.5*k);
            temp2 = (sig[i] + wn*sig[i+N/2]);
            temp3 = temp1 * temp2;
            sig_fft[k] = sig_fft[k] + temp3;
        }
    }
    
    return sig_fft;
}*/


template <typename T=Complex<double> >
vector<T> fft(vector<T> sig, int N=256)
{
    vector<Complex<double> > sig_fft(N);
    Complex<double> wn;
    vector<Complex<double> > temp(N);
    vector<Complex<double> > temp1(N/2);
    int size;
    
    for (int i = 0; i < N; i++)
    {
        int temp_var1=1, temp_var2=0, temp_var3;
        temp_var3 = i;
        for (int p = 0; p < log2(N); p++)
        {
             temp_var2 |= temp_var1 & temp_var3;
             temp_var3 = temp_var3>>1;
             temp_var2 = temp_var2<<1;
        }
        temp_var2 = temp_var2>>1;
        temp[i] = sig[temp_var2];
    }

    for (int k = 0; k < N; k++)
    {
        for (int m = 1; m < log2(N)+1; m++)
        {
            size = N/pow(2,m);
            for (int l = 0; l < size; l++)
            {
                wn.polar_complex((double) (-2)*pi*k*size/N);
                if(m==1)
                    temp1[l] = temp[2*l] + wn * temp[2*l+1];
                else
                    temp1[l] = temp1[2*l] + wn * temp1[2*l+1];
            }
        }
        
        sig_fft[k] = temp1[0];
        //sig_fft[N-k-1] = temp1[0];
    }
 
    return sig_fft;
}


int main()
{
    Complex<double> x(1,0), y(5,6);
    vector<Complex<double> > sig(256);
    sig[0](1,0);
    Complex<double> z(0,0);

    for (int i = 1; i < 256; i++)
    {
        y = sig[i-1];
        sig[i] = y + x;
    }
    
    
    
    //for (int j = 0; j < 16; j++)
    //   cout <<sig[j] <<endl;
    
    cout << "starting\n";
    vector<Complex<double> > r =  fft(sig, 256);
    
    for (int j = 0; j < 256; j++)
        cout << r[j];
}




