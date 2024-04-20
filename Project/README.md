# Weak primes in RSA private key - Fermat's factorization method

- The RSA modulus is constructed from two "random" prime numbers
- For the special case where the primes are close, [Fermat's factorization method](https://eprint.iacr.org/2023/026.pdf) can be applied to factor the modulus with ease
- However, for a 2048-bit key, this works only if the first approx. 500 bits of the prime factors are identical
- The probability of this happening on a properly implemented random prime generator is approx. 1 in 2<sup>500</sup>
- Only feasible if the above constraint is satisfied, else computationally expensive(infeasible?)
- References:
  - Hanno B¨ock. 2023. Fermat Factorization in the Wild. *Cryptology ePrint Archive, Paper 2023/026* - https://eprint.iacr.org/2023/026.pdf
