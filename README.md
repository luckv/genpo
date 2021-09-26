# Genpo

A python library and a simple CLI program to generate and manipulate polynomials with roots simple to find by hand. The degree of the polynomial, the number of roots and the multiplicities of these roots, are all tweakable to generate polynomials with different grades of difficulty.

I started this library while studying for a math exam where it was required to quickly find the roots of a polynomial of degree 3 or 4. It helped me pass it.

## Genpo library

### Polynomials as arrays

The polynomials in this library are all represented as arrays, in which the element at position `i` in the array is the coefficient of `x^i`.  I chose this representation because its simple to understand and manipulate. I didn't wrap it in a class because I think it would only create unnecessary complexity.

The genpo library modules are mainly divided in 2 section: manipulation and random generators.

## Manipulation modules

These modules provide functions to manipulate polynomials: creation, arithmetic operations and string representations

### genpo.polynomials

Pure functions for creating polynomials from parameters

### genpo.operations

Do arithmetic operations on polynomials.

Operations actually supported:

- sum between polynomials
- multiplication between polynomials
- multiplication of a polynomial by a factor
- evaluation of a polynomial and its derivative in one point

### genpo.roots

Utilities functions to work with roots and multiplicities.

### genpo.representation

String representations of polynomials. Thought to be printed in the terminal


## Genpo cli 

Coming soon. Stay tuned ;)

