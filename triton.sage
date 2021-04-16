#!/usr/bin/env sage

p = 0x24000000000024000130e0000d7f70e4a803ca76f439266f443f9a5cda8a6c7be4a7a5fe8fadffd6a2a7e8c30006b9459ffffcd300000001
q = 0x24000000000024000130e0000d7f70e4a803ca76f439266f443f9a5c7a8a6c7be4a775fe8e177fd69ca7e85d60050af41ffffcd300000001

Fp2.<x> = GF(p^2, modulus=x^2 + 5)
Fp = GF(p)
Ep = EllipticCurve(Fp, [0, 57])
assert Ep.count_points() == q

for i in range(1, 3):
    E_not_triton = EllipticCurve(Fp2, [0, x+i])
    r = E_not_triton.count_points()
    assert q*(2*p - q) != r  # wrong twist

E_triton = EllipticCurve(Fp2, [0, x+3])
r = E_triton.count_points()
assert q*(2*p - q) == r  # right twist

print("Checked Triton parameters.")
