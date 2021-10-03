# Genpo

A python library and a simple CLI program to generate and manipulate polynomials with roots simple to find by hand. The degree of the polynomial, the number of roots and the multiplicities of these roots, are all tweakable to generate polynomials with different grades of difficulty.

I started this library while studying for a math exam where it was required to quickly find the roots of a polynomial of degree 3 or 4. It helped me pass it.

# Python library

## Polynomials as arrays

The polynomials in this library are all represented as arrays, in which the element at position `i` in the array is the coefficient of `x^i`.  I chose this representation because its simple to understand and manipulate. I didn't wrap it in a class because I think it would only create unnecessary complexity.

## Modules

The genpo library modules are mainly divided in 2 section: manipulation and random generators.

## Manipulation modules

These modules provide functions to manipulate polynomials: creation, arithmetic operations and string representations

### `genpo.polynomials`

Pure functions for creating polynomials from parameters

### `genpo.operations`

Do arithmetic operations on polynomials.

Operations actually supported:

- sum between polynomials
- multiplication between polynomials
- multiplication of a polynomial by a factor
- evaluation of a polynomial and its derivative in one point

### `genpo.roots`

Utilities functions to work with roots and multiplicities.

### `genpo.representation`

String representations of polynomials. Code thought to be printed in the terminal

## Random generators (`genpo.random`)
All modules under `genpo.random` have the scope of generating random roots and polynomials. All values generated are roots simple to find and values easy to calculate for a person that is resolving a polynomial by hand.

### `values`

Generators for intervals of values, simple fractions or expanding randomly a list of items. This module is used internally in more complex generators

### `roots`

Generators for random polynomials roots and multiplicities. All generated roots are integers numbers not too big. They are simple to find.

### `polynomials`

Generators for polynomials, with or without roots. This is the core of the genpo library, where many parts of the library are used. The functions in this file are divided in two categories: generators for polynomials in which the sum of multiplicities of their zeroes equals its degree, and generators for polynomials with an arbitrary sum of zeroes' multiplicity.

#### `fz` generators

Functions in the `genpo.random.polynomials` with `fz` in the name, are functions that returns polynomials that I defined *full zeroes*, polynomials in which the sum of multiplicities of their zeroes equals its degree.


# Genpo cli

Coming soon. Stay tuned ;)

