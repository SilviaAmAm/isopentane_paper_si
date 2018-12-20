geomtyp=xyz

nosym
noorient
gdirect
angstrom

geometry=input.xyz

set,charge=0

basis=svp
{cf-uks,pbe;}
{optg,method=slrf,maxiter=50;
constraint,1.000,angstrom,bond,atoms=[H7,C1]
constraint,2.700,angstrom,bond,atoms=[H7,C17]
constraint,180,deg,angle,atoms=[C1,H7,C17]
{slopt;}}
{cf-uks,pbe0;}
{optg,method=slrf,maxiter=20;
constraint,1.000,angstrom,bond,atoms=[H7,C1]
constraint,2.700,angstrom,bond,atoms=[H7,C17]
constraint,180,deg,angle,atoms=[C1,H7,C17]
{slopt;}}
basis=tzvp
{cf-uks,pbe;}
force
