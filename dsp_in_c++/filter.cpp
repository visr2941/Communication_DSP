#include <iostream>
#include <vector>


template <typename type=float>
class FIR_Filter
{
	type *coef;	//pointer to coefficients of filter
	int length;		//size of the filter
	string winType;	//type of window
	
public:
	FIR_Filter(): coef(NULL), length(0), winType("ham") {}
	~FIR_Filter() {	if (coef != NULL) delete coef; }
	
	type * GenerateCoef(string &);	//function to generate the coefficient 
	vector<type> Filter(const vector<type> &dataIn);	//to filter the data
	int Length() const;		//to return length of the filter
}