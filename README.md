# Pluto/Eris supporting evidence

This repository contains supporting evidence on the security of the half-pairing
cycle of prime-order curves:

* Ep : y<sup>2</sup> = x<sup>3</sup> + 57 over GF(p) of order q, called Pluto;
* Eq : y<sup>2</sup> = x<sup>3</sup> + 57 over GF(q) of order p, called Eris;

with

* p = 0x24000000000024000130e0000d7f70e4a803ca76f439266f443f9a5cda8a6c7be4a7a5fe8fadffd6a2a7e8c30006b9459ffffcd300000001
* q = 0x24000000000024000130e0000d7f70e4a803ca76f439266f443f9a5c7a8a6c7be4a775fe8e177fd69ca7e85d60050af41ffffcd300000001

Pluto is a Barreto–Naehrig (BN) pairing-friendly curve, with embedding degree 12.
Eris is a non-pairing-friendly curve.

The BN parameter for Pluto (used in pairing implementation) is:

* u = -0x4000000000001000008780000000

If we represent GF(p<sup>2</sup>) as GF(p)[z]/(z<sup>2</sup> + 5), then the curve
Ep' used for G<sub>2</sub> is:

* Ep' : y<sup>2</sup> = x<sup>3</sup> + (z + 3) over GF(p<sup>2</sup>) of
  order q·(2·p - q), called Triton.

(This definition of Triton has not been finalized and is subject to change.)


## Security and engineering properties

The size of 446 bits follows
[recommendations by Aurore Guillevic](https://members.loria.fr/AGuillevic/pairing-friendly-curves/)
for BN curves at the 128-bit security level (but any errors are my own).
More precisely, by using the STNFS cost simulator associated with [[GS2019]], we obtain
an estimate of roughly 132 bits of security for Pluto, Triton, and their pairing.
The security margin of Eris is larger since attacks on the pairing are not applicable:
it has a Pollard rho security level of 221.6 bits.

446 bits is the maximum that can be implemented in seven 64-bit limbs, with two bits
to spare for carries, which provides a good security/efficiency trade-off. The "spare"
two bits can also for used for infinity and compressed y-coordinate flags in a 56-byte
point representation.

Both curves have j-invariant 0, enabling use of endomorphisms for scalar multiplication
in a similar way to the [Pasta curves](https://github.com/zcash/pasta) and to secp256k1.
The values ζ<sub>p</sub> and ζ<sub>q</sub> used in these endomorphisms are of length 335
or 336 bits, which is only 3/4 of the field size; this allows a particularly efficient
implementation of scalar multiplications by partially random scalars with entropy
up to ~220 bits.

Each curve has an isogeny of degree 3 from a curve with j-invariant not equal to 0 or 1728,
allowing use of the "simplified SWU" method for hashing to an elliptic curve. This is based
on code from Appendix A of [[WB2019](https://eprint.iacr.org/2019/403.pdf)].

Both curves have a 2-adicity of 32 (i.e. 2<sup>32</sup> divides p-1 and q-1), which
enables support for fast FFT operations, used in many zero-knowledge proving systems.

The parameter u has low Hamming weight (7), to speed up pairing computations.
It can be expressed in [2-NAF form](https://en.wikipedia.org/wiki/Non-adjacent_form) as
-(2<sup>110</sup> + 2<sup>60</sup> + 2<sup>39</sup> + 2<sup>35</sup> - 2<sup>31</sup>)
which has weight 5.

Both curves are twist-secure to over 149 bits.

α is relatively prime to each of p-1 and q-1 for α ∊ {5, 7, 11, 13}, allowing use
of x<sup>α</sup> for those values as an S-box in algebraic hashes such as Poseidon and
Rescue.


## Applications

Half-pairing cycles are potentially useful to combine Halo-style recursion
[[BGH2019](https://eprint.iacr.org/2019/1021)] [[BCMS2020](https://eprint.iacr.org/2020/499)]
[[BDFG2020](https://eprint.iacr.org/2020/1536)] [[BCLMS2020](https://eprint.iacr.org/2020/1618)]
with any protocol that uses pairings.

That could include pairing-based proving systems with trusted setup such as Groth16 and
PLONK, but it could also include schemes without trusted setup such as BLS signatures,
some identity-based or forward-secure encryption schemes, tripartite Diffie–Hellman, and
[[BMMTV](https://eprint.iacr.org/2019/1177)] polynomial commitments.

Significant additional research and engineering work might be needed to adapt any
particular protocol to this setting. If you don't need the pairing, use
[Pallas/Vesta](https://github.com/zcash/pasta) instead — it will be simpler and more
efficient!


## Naming

Pluto and Eris are [planets](https://www.hou.usra.edu/meetings/lpsc2017/pdf/1448.pdf)
in the solar system's Kuiper belt. They are close in size and mass; Pluto is slightly
larger (about 32% the volume of Earth's moon vs Eris' 30%), and Eris is slightly more
massive (about 22% the mass of Earth's moon vs Pluto's 18%).

Correspondingly, the Pluto curve is defined over the larger base field than the
Eris curve (p > q), but has the smaller order. The name of the Pluto curve starts
with 'P' which is mnemonic for pairing-friendly.

Triton is originally another Kuiper belt object, larger than Pluto, that was captured
as a satellite of Neptune.


## Generation

Pluto/Eris is the first cycle output by
``sage halfpairing.sage --sequential --requireisos --sortqp 446 32``.

(The `--sequential` option makes the output completely deterministic and so resolves
ambiguity about which result is "first". For exploratory searches it is faster not to
use `--sequential`.)

The output of ``halfpairing.sage`` with the above options includes the isogenies of
degree 3 mentioned above.

Prerequisites:

* ``apt-get install sagemath``

Run ``sage verify.sage Ep`` and ``sage verify.sage Eq`` to test each curve against
[SafeCurves criteria](https://safecurves.cr.yp.to/index.html); or ``./run.sh`` to test
both curves and also print out the results.

The SafeCurves criteria that are *not* satisfied are, in summary:

* large-magnitude CM discriminant (both curves have CM discriminant of absolute value 3,
  as a consequence of how they were constructed);
* completeness (complete formulae are possible, but not according to the Safe curves
  criterion);
* ladder support (not possible for prime-order curves);
* Elligator 2 support (indistinguishability is possible using
  [Elligator Squared](https://ifca.ai/pub/fc14/paper_25.pdf), but not using Elligator 2);
* Pluto is pairing-friendly and therefore cannot satisfy the embedding degree criterion.

To check the estimated cost of a STNFS attack against the Pluto curve, you will need the
(experimental) software supporting the paper [[GS2019]] by Aurore Guillevic and Shashank Singh:

* run ``git clone https://gitlab.inria.fr/tnfs-alpha/alpha.git`` (the resulting checkout
  must be in the ``alpha`` subdirectory of this repo).
* run ``./check_stnfs.sh``.

The special form of the prime p and the presence of endomorphisms for BN curves is taken
into account.

Note that this script requires a version of Sage that uses Python 3 (unlike the other
Sage scripts in this repo that can work with versions of Sage using either Python 2 or 3).
It takes several hours to run, and the output is quite verbose. The estimated security
level against STNFS is given by the minimum of the "total time" outputs.

[GS2019]: https://eprint.iacr.org/2019/885
