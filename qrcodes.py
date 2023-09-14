"""
QR Code Generator
"""

import comp140_module5 as qrcode
import comp140_module5_z256 as z256
from collections import defaultdict

def divide_terms(coefficient1, power1, coefficient2, power2):
    """
    Computes the quotient of two terms.

    The degree of the first term, power1, must be greater than or
    equal to the degree of the second term, power2.

    Inputs:
        - coefficient1: a Z_256 number representing the coefficient of the first polynomial term
        - power1: an integer representing the power of the first term.
        - coefficient2: a Z_256 number representing the coefficient of the second polynomial term
        - power2: an integer representing the power of the second term.

    Returns: an instance of a Polynomial that is the resulting
    term.
    """
    # From recipe: (a*x^b) / (c*x^d) = (a/c) * x^(b-d)
    new_coeff = z256.div(coefficient1, coefficient2)
    new_pow = power1 - power2

    # Represent our answer as a Polynomial
    divided = Polynomial()
    divided = divided.add_term(new_coeff, new_pow)
    return divided

class Polynomial:
    """
    A class used to abstract methods on a polynomial in the finite
    field Z_256 (including numbers from 0 through 255).

    Since 256 is not prime, but is rather of the form p^n = 2^8, this
    representation uses special arithmetic via the z256 module so as to
    preserve multiplicative inverses (division) inside this field.
    """

    def __init__(self, terms=None):
        """
        Creates a new Polynomial object.  If a dictionary of terms is provided,
        they will be the terms of the polynomial,
        otherwise the polynomial will be the 0 polynomial.

        inputs:
            - terms: a dictionary of terms mapping powers to coefficients or None
              (None indicates that all coefficients are 0)
        """
        if terms != None:
            self._terms = dict(terms)
        else:
            self._terms = {}

    def __str__(self):
        """
        Returns: a string representation of the polynomial, containing the
        class name and all of the terms.
        """
        # Create a string of the form "ax^n + bx^n-1 + ... + c" by
        # creating a string representation of each term, and inserting
        # " + " in between each
        term_strings = []

        # Add the highest powers first
        powers = list(self._terms.keys())
        powers.sort(reverse=True)
        for power in powers:
            coefficient = self._terms[power]
            # Don't print out terms with a zero coefficient
            if coefficient != 0:
                # Don't print "x^0"; that just means it's a constant
                if power == 0:
                    term_strings.append("%d" % coefficient)
                else:
                    term_strings.append("%d*x^%d" % (coefficient, power))

        terms_str = " + ".join(term_strings)
        if terms_str == "":
            terms_str = "0"
        return "Polynomial: %s" % terms_str

    def __eq__(self, other_polynomial):
        """
        Check if another polynomial is equvalent

        inputs:
            - other_polynomial: a Polynomial object

        Returns a boolean: True if other_polynomial contains
        the same terms as self, False otherwise.
        """
        # Make sure that other_polynomial is a Polynomial
        if not isinstance(other_polynomial, Polynomial):
            return False

        # Get the terms of the other_polynomial
        terms = other_polynomial.get_terms()

        # Check that all terms in other_polynomial appear in self
        for power, coefficient in terms.items():
            if coefficient != 0:
                if power not in self._terms:
                    return False
                if self._terms[power] != coefficient:
                    return False

        # Check that all terms in self appear in other_polynomial
        for power, coefficient in self._terms.items():
            if coefficient != 0:
                if power not in terms:
                    return False
                if terms[power] != coefficient:
                    return False

        return True

    def __ne__(self, other_polynomial):
        """
        Check if another polynomial is NOT equivalent

        inputs:
            - other_polynomial: a Polynomial object

        Return a boolean: False if other_polynomial contains the same terms
        as self, True otherwise.
        """
        return not self.__eq__(other_polynomial)

    def get_terms(self):
        """
        Returns: a dictionary of terms, mapping powers to coefficients.
        This dictionary is a completely new object and is not a reference
        to any internal structures.
        """
        terms = dict(self._terms)
        return terms

    def get_degree(self):
        """
        Returns: the maximum power over all terms in this polynomial.
        """
        # Since we don't clean zero-coefficient powers out of our dictionary,
        # we need a trickier get_degree function, to take into account that
        # some coefficients could be zero.
        highest_power = 0
        for power in self._terms:
            if (power > highest_power) and (self._terms[power] != 0):
                highest_power = power

        return highest_power


    def get_coefficient(self, power):
        """
        Determines the coefficient of x^(power) in this polynomial.
        If there is no coefficient of x^(power), this method
        returns 0.

        inputs:
            - power: an integer representing a polynomial power

        Returns: a Z_256 number that is the coefficient or 0 if there
                 is no term of the given power
        """
        if power in self._terms:
            return self._terms[power]
        else:
            return 0

    def add_term(self, coefficient, power):
        """
        Add one term to this polynomial.

        inputs:
            - coefficient: a Z_256 number representing the coefficient of the term
            - power: an integer representing the power of the term

        Returns: a new Polynomial that is the sum of adding this polynomial
        to (coefficient) * x^(power) using Z_256 arithmetic to add
        coefficients, if necessary.
        """
        # Replace with your code for part 3.A
#create a new dictionary that initially represents the same polynomial
#as the given polynomial, but eventually becomes the representation
#for the added polynomial
        new_terms = defaultdict(int)
        poly_dict = self.get_terms()
        for powe, coeff in poly_dict.items():
            new_terms[powe] = coeff
        current_coeff = new_terms[power]
        new_terms[power] = z256.add(current_coeff, coefficient)
        added_poly = Polynomial(new_terms)
        return added_poly

    def subtract_term(self, coefficient, power):
        """
        Subtract one term from this polynomial.

        inputs:
            - coefficient: a Z_256 number representing the coefficient of the term
            - power: an integer representing the power of the term

        Returns: a new Polynomial that is the difference of this polynomial
        and (coefficient) * x^(power) using Z_256 arithmetic to subtract
        coefficients, if necessary.
        """
        # Replace with your code for part 3.B
#similar to above
        new_terms = defaultdict(int)
        poly_dict = self.get_terms()
        for powe, coeff in poly_dict.items():
            new_terms[powe] = coeff
        current_coeff = new_terms[power]
        new_terms[power] = z256.sub(current_coeff, coefficient)
        subtracted_poly = Polynomial(new_terms)
        return subtracted_poly

    def multiply_by_term(self, coefficient, power):
        """
        Multiply this polynomial by one term.

        inputs:
            - coefficient: a Z_256 number representing the coefficient of the term
            - power: an integer representing the power of the term

        Returns: a new Polynomial that is the product of multiplying
        this polynomial by (coefficient) * x^(power).
        """
        # Replace with your code for part 3.C
        mul_terms = {}
#take the given power and coefficient and multiply it to each term in 
#the given polynomial
        poly_dict = self.get_terms()
        for powe, coeff in poly_dict.items():
            mul_terms[power + powe] = z256.mul(coefficient, coeff)
        mul_poly = Polynomial(mul_terms)
        return mul_poly

    def add_polynomial(self, other_polynomial):
        """
        Compute the sum of the current polynomial other_polynomial.

        inputs:
            - other_polynomial: a Polynomial object

        Returns: a new Polynomial that is the sum of both polynomials.
        """
        # Replace with your code for part 4.A
        poly_dict = self.get_terms()
        added_poly = Polynomial(poly_dict)
        poly2_terms = other_polynomial.get_terms()
#add each term in the other polynomial to the given polynomial
        for powe, coeff in poly2_terms.items():
            added_poly = added_poly.add_term(coeff, powe)
        return added_poly
        
    def subtract_polynomial(self, other_polynomial):
        """
        Compute the difference of the current polynomial and other_polynomial.

        inputs:
            - other_polynomial: a Polynomial object

        Returns: a new Polynomial that is the difference of both polynomials.
        """
        # Replace with your code for part 4.B
#similar to above
        poly_dict = self.get_terms()
        sub_poly = Polynomial(poly_dict)
        poly2_terms = other_polynomial.get_terms()
        for powe, coeff in poly2_terms.items():
            sub_poly = sub_poly.add_term(coeff, powe)
        return sub_poly

    def multiply_by_polynomial(self, other_polynomial):
        """
        Compute the product of the current polynomial and other_polynomial.

        inputs:
            - other_polynomial: a Polynomial object

        Returns: a new Polynomial that is the product of both polynomials.
        """
        # Replace with your code for part 4.C
        mul_poly = Polynomial()
        poly2_terms = other_polynomial.get_terms()
#multiply each term of the other polynomial with the given polynomial
#and add the products
        for powe, coeff in poly2_terms.items():
            mul_poly = mul_poly.add_polynomial(self.multiply_by_term(coeff, powe))
        return mul_poly

    def remainder(self, denominator):
        """
        Compute a new Polynomial that is the remainder after dividing this
        polynomial by denominator.

        Note: does *not* return the quotient; only the remainder!

        inputs:
            - denominator: a Polynomial object

        Returns: a new polynomial that is the remainder
        """
        # Replace with your code for part 4.D
#track the current numerator used to be divided by the denominator
        poly_dict = self.get_terms()
        cur_nume = Polynomial(poly_dict)
        n_degree = cur_nume.get_degree()
        n_coeff = cur_nume.get_coefficient(n_degree)
        d_degree = denominator.get_degree()
        d_coeff = denominator.get_coefficient(d_degree)
#keep dividing as long as the numerator's degree >= the denominator's degree
        while n_degree >= d_degree:
            quo = divide_terms(n_coeff, n_degree, d_coeff, d_degree)
            next_cur = quo.multiply_by_polynomial(denominator)
            cur_nume = cur_nume.subtract_polynomial(next_cur)
            n_degree = cur_nume.get_degree()
            n_coeff = cur_nume.get_coefficient(n_degree)
#if the current numerator is 0 then the remainder of the division is 0
            if n_coeff == 0:
                return cur_nume
        return cur_nume
    
def create_message_polynomial(message, num_correction_bytes):
    """
    Creates the appropriate Polynomial to represent the
    given message. Relies on the number of error correction
    bytes (k). The message polynomial is of the form
    message[i]*x^(n+k-i-1) for each number/byte in the message.

    Inputs:
        - message: a list of integers (each between 0-255) representing data
        - num_correction_bytes: an integer representing the number of
          error correction bytes to use

    Returns: a Polynomial with the appropriate terms to represent the
    message with the specified level of error correction.
    """
    # Replace with your code for part 5.A
    msg = {}
#follow the formula for the message polynomial
    for idx in range(len(message)):
        msg[num_correction_bytes + len(message) - idx - 1] = message[idx]
    msg_poly = Polynomial(msg)
    return msg_poly

def create_generator_polynomial(num_correction_bytes):
    """
    Generates a static generator Polynomial for error
    correction, which is the product of (x-2^i) for all i in the
    set {0, 1, ..., num_correction_bytes - 1}.

    Inputs:
        - num_correction_bytes: desired number of error correction bytes.
                                In the formula, this is represented as k.

    Returns: generator Polynomial for generating Reed-Solomon encoding data.
    """
    # Replace with your code for part 5.B
#follow the formula for generator polynomial
    gen_poly = Polynomial({0: 1})
    for idx in range(num_correction_bytes):
        next_num = defaultdict(int)
        next_num[1] = 1
        next_num[0] += z256.power(2, idx)
        gen_poly = gen_poly.multiply_by_polynomial(Polynomial(next_num))
    return gen_poly

def reed_solomon_correction(encoded_data, num_correction_bytes):
    """
    Corrects the encoded data using Reed-Solomon error correction

    Inputs:
        - encoded_data: a list of integers (each between 0-255)
                        representing an encoded QR message.
        - num_correction_bytes: desired number of error correction bytes.

    Returns: a polynomial that represents the Reed-Solomon error
    correction code for the input data.
    """
    # Replace with your code for part 5.C
#find the remainder of dividing the message by the generator polynomial 
    msg_poly = create_message_polynomial(encoded_data, num_correction_bytes)
    gen_poly = create_generator_polynomial(num_correction_bytes)
    reed = msg_poly.remainder(gen_poly)
    return reed


# Uncomment the following line when you are ready to generate an
# actual QR code.  To do so, you must enter a short message in the
# "info" text box and hit return (be sure to hit return!).  You then
# must push the "Generate!" button.  This will generate a QR code for
# you to view - try scanning it with your phone!  If you would like to
# save your QR codes, you can use the "Image in a New Window" button
# to create a .png file that you can save by right clicking in your
# browser window.

# qrcode.start(reed_solomon_correction)
