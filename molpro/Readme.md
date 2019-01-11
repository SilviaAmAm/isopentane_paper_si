# Molpro input files

[constrained_optimization.com](constrained_optimization.com) is an example Molpro input file for doing constrained optimization on a structure with PBE0/SVP, followed by a energy and force evaluation with PBE/TZVP.

[single_point.com](single_point.com) is a Molpro input file for doing a energy and force evaluation with PBE/TZVP.

[input.xyz](input.xyz) contains the structure used for the computations. The atoms are named to make the input format for the constrained optimizations simpler.

## Scripts to automate generation of input files
A [separate repo](https://github.com/larsbratholm/constrained_md) holds the scripts to automate the generation of input files for a grid of constraints. The commit used for this paper was 61bea77.
The example `make_opt_input.py` creates molpro input files for the constraint grid described in the paper. The script does a constrained force field optimization with openbabel to generate the initial structures, however the same initial structure was eventually used in the paper.

