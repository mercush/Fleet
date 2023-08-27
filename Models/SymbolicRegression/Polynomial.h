#pragma once

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Compute polynomial degrees
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#include <vector>

/* This class stores the degree of a polynomial and a bool that indicates whether
 * its a degree or a constant (which is somemtimes used in computing the degree). When
 * we end up with a non-polynomial, we return NaN */

// TODO: We could rewrite this to define two subclasses of polynomial degrees (constants and powers) 
//       and then define arithmetic on them...

class Polydeg {
public:
    double value; //
    bool   is_const; //if true, value is a constant, otherwise it is an exponent on x
    Polydeg(double v, bool b) : value(v), is_const(b) {
    }
	bool isnan() { return std::isnan(value); }
};


Polydeg get_polynomial_degree_rec(const Node& n, const std::vector<Constant>& constants, size_t cidx) {
	
	const std::string fmt = n.rule->format;
	
    if(fmt == "(%s+%s)") {
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx); 
        Polydeg v2 = get_polynomial_degree_rec(n.child(1), constants, cidx);
		if(v1.isnan() or v2.isnan()) return Polydeg(NaN,false); // doesn't matter whether its const or not
        else if(v1.is_const && v2.is_const) return Polydeg(v1.value+v2.value, true); // if both consts, then return their value
        else if (v1.is_const) return v2; // we can't let cosntants/nans interfere here
        else if (v2.is_const) return v1;
        else return Polydeg(std::max(v1.value,v2.value), false);
    }
	else if(fmt == "(%s-%s)") {
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
        Polydeg v2 = get_polynomial_degree_rec(n.child(1), constants, cidx);
		if(v1.isnan() or v2.isnan()) return Polydeg(NaN,false); 
        else if(v1.is_const && v2.is_const) return Polydeg(v1.value-v2.value, true); // if both consts, then return their value
        else if (v1.is_const) return v2;
        else if (v2.is_const) return v1;
        else return Polydeg(std::max(v1.value,v2.value), false);
    }
    else if(fmt == "(%s*%s)") {
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
        Polydeg v2 = get_polynomial_degree_rec(n.child(1), constants, cidx);
		if(v1.isnan() or v2.isnan()) return Polydeg(NaN,false); 
        else if(v1.is_const && v2.is_const) return Polydeg(v1.value*v2.value,true); // if boths consts, then return their value
        else if(v1.is_const) return v2; // otherwise we ignore constants
        else if(v2.is_const) return v1;
        else return Polydeg(v1.value+v2.value,false); // both are powers so they add
    }
    else if(fmt == "(%s/%s)") {
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
        Polydeg v2 = get_polynomial_degree_rec(n.child(1), constants, cidx);
		if(v1.isnan() or v2.isnan()) return Polydeg(NaN,false); 
        else if(v1.is_const && v2.is_const) return Polydeg(v1.value/v2.value,true); // if boths consts, then return their value
        else if(v1.is_const) return Polydeg(NaN, false); // negative powers not allowed -- since otherwise things like x/(1+x) are counted as polynomials
        else if(v2.is_const) return v1; // v1 is an exponent, constant doesn't matter
        return Polydeg(NaN,true); 
    }
    else if(fmt == "(%s^%s)" or fmt == "pow_abs(%s,%s)") { // either format allowed
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
        Polydeg v2 = get_polynomial_degree_rec(n.child(1), constants, cidx);
		if(v1.isnan() or v2.isnan()) return Polydeg(NaN,false); 
        else if(v1.is_const && v2.is_const) return Polydeg(pow(std::abs(v1.value),v2.value),true); // if both constants, take their power
        else if(v1.is_const) return Polydeg(NaN,false); // 2.3 ^ x -- not a polynomial
        else if(v2.is_const) return Polydeg(std::abs(v1.value)*v2.value,false); // x^{2.3} -- is a polynomial, so multiply the exponents
        return Polydeg(NaN,false); // both are exponents but not a polynomial so forget it
    }
    else if(fmt == "(-%s)") {
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
		if(v1.isnan()) return Polydeg(NaN,false); 
		else if(v1.is_const) return Polydeg(-v1.value, true);
		else            return v1;
    }
    else if(fmt == "x" or 
			(fmt[0] == '%' and fmt[1]=='s' and fmt.size()<=4) or 
			(fmt[0] == 'x' and fmt.size() == 2)) { // x or %s1 %s2, %s3, etc 
        return Polydeg(1.0, false);
    }
	else if(fmt == "C") { 
        return Polydeg(constants.at(cidx++), true);
    }
	else if(fmt == "1") {
        return Polydeg(1.0, true);
    }
	else if(fmt == "2") {
        return Polydeg(2.0, true);
    }
	else if(fmt == "3") {
        return Polydeg(3.0, true);
    }
	else if(fmt == "0.5") {
        return Polydeg(0.5, true);
    }
	else if(fmt == "pi") {
        return Polydeg(M_PI, true);
    }
	else if(fmt == "tau") {
        return Polydeg(2*M_PI, true);
    }
	else if(fmt == "log(%s)") { 
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
        if(v1.isnan()) return Polydeg(NaN,false); 
		else if(v1.is_const) return Polydeg(log(v1.value), true); // handles cases like x^exp(3)
        else            return Polydeg(NaN,false);
    }
	else if(fmt == "exp(%s)") { 
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
		if(v1.isnan()) return Polydeg(NaN,false); 
		else if(v1.is_const) return Polydeg(exp(v1.value), true);
        else            return Polydeg(NaN,false);
    }
	else if(fmt == "expm(%s)") { 
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
		if(v1.isnan()) return Polydeg(NaN,false); 
		else if(v1.is_const) return Polydeg(exp(-v1.value), true);
        else            return Polydeg(NaN,false);
    }
	else if(fmt == "asin(%s)") { 
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
		if(v1.isnan()) return Polydeg(NaN,false); 
		else if(v1.is_const) return Polydeg(asin(v1.value), true);
        else            return Polydeg(NaN,false);
    }
	else if(fmt == "sin(%s)") { 
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
		if(v1.isnan()) return Polydeg(NaN,false); 
		else if(v1.is_const) return Polydeg(sin(v1.value), true);
        else            return Polydeg(NaN,false);
    }
	else if(fmt == "cos(%s)") { 
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
		if(v1.isnan()) return Polydeg(NaN,false); 
		else if(v1.is_const) return Polydeg(cos(v1.value), true);
        else            return Polydeg(NaN,false);
    }
	else if(fmt == "sq(%s)") {
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
		if(v1.isnan()) return Polydeg(NaN,false); 
		else if(v1.is_const) return Polydeg(v1.value*v1.value, true);
		else                 return Polydeg(2*v1.value, false);
    }
	else if(fmt == "sqrt_abs(%s)") {
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
		if(v1.isnan()) return Polydeg(NaN,false); 
		else if(v1.is_const) return Polydeg(std::sqrt(std::abs(v1.value)), true);
		else                 return Polydeg(0.5*std::abs(v1.value), false);
    }
	else if(fmt == "pow_abs(%s,2)") {
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
		if(v1.isnan()) return Polydeg(NaN,false); 
		else if(v1.is_const) return Polydeg(powf(std::abs(v1.value),2), true);
		else                 return Polydeg(2*std::abs(v1.value), false);
    }
	else if(fmt == "pow_abs(%s,3)") {
        Polydeg v1 = get_polynomial_degree_rec(n.child(0), constants, cidx);
		if(v1.isnan()) return Polydeg(NaN,false); 
		else if(v1.is_const) return Polydeg(powf(std::abs(v1.value),3), true);
		else                 return Polydeg(3*std::abs(v1.value), false);
    }
	else {
		print("In format string: ", fmt);
		assert(false && "*** Unmatched format string by polynomial. Did you change the primitives and not update this?");
	}
}

double get_polynomial_degree(const Node& n, const std::vector<Constant>& constants) {
	size_t cidx = 0;
    Polydeg r = get_polynomial_degree_rec(n, constants, cidx);
	if(r.isnan()) return NaN;
	else          return (r.is_const ? 0.0 : r.value);
}
