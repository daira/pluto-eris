#!/bin/sh
sage verify.sage Ep
sage verify.sage Eq

echo ""
echo "Ep (Pluto)"
echo "----------"
grep -Rn '.' Ep/verify-* |grep '^Ep/verify-.*:1:' |sed 's/:1:/ = /'
echo ""
echo "Eq (Eris)"
echo "---------"
grep -Rn '.' Eq/verify-* |grep '^Eq/verify-.*:1:' |sed 's/:1:/ = /'

