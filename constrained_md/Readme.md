# Molpro input files

[example.inp](example.inp) is an example CP2K input file for doing constrained MD with PM6.

[example.xyz](example.xyz) contains the structure used for the computations.

## Scripts to automate generation of input files
A [separate repo](https://github.com/larsbratholm/constrained_md) holds the scripts to automate the generation of input files for a grid of constraints. The commit used for this paper was 61bea77.
The example `make_md_input.py` creates CP2K input files for the constraint grid described in the paper. The script does a constrained force field optimization with openbabel to generate the initial structures.
