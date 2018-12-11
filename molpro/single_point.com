geomtyp=xyz

nosym
noorient
gdirect
angstrom

geometry=input.xyz

set,charge=0

basis=tzvp
{cf-uks,pbe;}
force
