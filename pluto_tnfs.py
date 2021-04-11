# This is <https://gitlab.inria.fr/tnfs-alpha/alpha/-/blob/master/sage/example_bn_254.py>
# adapted for the Pluto curve.
#
# It needs to be loaded from Sage, and is dependent on other files from the above repo:
#
#   git clone https://gitlab.inria.fr/tnfs-alpha/alpha.git
#   ./check_tnfs.sh

import sys
assert sys.version_info[0] == 3, "This script requires Python 3."

from sage.all_cmdline import *   # import sage library

import sage
import tnfs
from tnfs.curve.bn import BN
from tnfs.simul.polyselect import Polyselect
from tnfs.simul.simulation_tnfs import Simulation_TNFS
from tnfs.alpha.alpha_tnfs_2d import alpha_TNFS_2d
from tnfs.simul.polyselect_utils import automorphism_factor
from tnfs.simul.polyselect_utils import pretty_print_coeffs_from_coeffs, pretty_print_poly_from_coeffs
from tnfs.param.testvector_sparseseed import test_vector_BN

# create curve
k=12
# see tnfs/param/testvector_sparseseed.py for other values
BN_data = {
  'u': -0x4000000000001000008780000000, 'b': 57, 'pnbits': 446,  'rnbits': 446, 'cost_S': 132, 'deg_h_S': 6, 'label': "Pluto"
}

seed = BN_data['u']
label = BN_data['label']
deg_h = BN_data['deg_h_S']
deg_g = k // deg_h
cost =  BN_data['cost_S']
E = BN(u=seed, b=BN_data['b'])
print(label)
print(E)
E.print_parameters()
# polynomial form of the parameters
px,rx,tx,cx,yx,betax,lambx,D = tnfs.curve.bn.polynomial_params()

# create an instance of Polyslect class
poly_init = Polyselect(E, deg_h=deg_h)
poly_init.compute_h(deg_h=deg_h)
list_h = poly_init.get_h()[deg_h]
for item in list_h:
    inv_zeta_Kh, w, hc = item
    hc_str = pretty_print_coeffs_from_coeffs(hc)
    h_str = pretty_print_poly_from_coeffs(hc)
    print("    ({0:.8f},{1:2d}, {2}), #{3}".format(float(inv_zeta_Kh), w, hc_str, h_str))
print("")

ZZy = ZZ['y']; (y,) = ZZy._first_ngens(1)

for item in list_h:
    inv_zeta_Kh, w, hc = item
    hc_str = pretty_print_coeffs_from_coeffs(hc)
    h_str = pretty_print_poly_from_coeffs(hc)
    print("    ({0:.8f},{1:2d}, {2}), #{3}".format(float(inv_zeta_Kh), w, hc_str, h_str))
    h = ZZy(hc)
    # Special Joux-Pierrot construction
    # since deg_h = 6, then deg_g = 12/6 = 2
    # since gcd(deg_h, deg_g) = 2 > 1, g should have algebraic coefficients: with_y=True
    res_poly = poly_init.TNFS_Special(deg_g=deg_g, h=h, poly_p=px, u=seed, with_y=True)
    if res_poly == None:
        raise ValueError("Error in Polynomial selection")
    f, g, max_fij, max_gij, aut_fg = res_poly
    print(f)
    print(g)
    print(h)

    p = E.p()
    ell = E.r()
    Fp = E.Fp()
    Fpz,z = E.Fpz()
    Rxy = f.parent()

    assert (ZZ(h.resultant(f.resultant(g))) % p**k) == 0

    if (gcd(deg_g,deg_h) == 1):
        aut_h = automorphism_factor(hc)
    else:
        aut_h = 1

    aut = aut_h*aut_fg

    # computing alpha, this takes at least a few seconds

    alpha_f = float(alpha_TNFS_2d(f,h,1000))
    alpha_g = float(alpha_TNFS_2d(g,h,1000))
    sum_alpha = alpha_f+alpha_g
    print("alpha_f = {:.4f} alpha_g = {:.4f} sum_alpha = {:.4f}".format(alpha_f,alpha_g,sum_alpha))

    # initialisation of data
    simul = Simulation_TNFS(p,ell,Fp,Fpz,h,f,g,Rxy,cost,aut,inv_zeta_Kh,count_sieving=True,alpha_f=alpha_f,alpha_g=alpha_g)

    simul.print_params()
    simul.simulation(samples=100000) #takes few seconds for 10^4, mins for 10^5, up to 20 min for 10^6
    simul.print_results()
    print("#::::::::::::::")
    # if there is not enough relations of there are too many relations, re-run with the same polynomials but with a higher/smaller cost
    simul.adjust_cost(samples=100000)
    print("############")
