# General Scripts

This folder contains the scripts used to calculate the results of the paper. It contains 4 types of scripts:

1. Generation of learning curves
2. Training of a single model and predicting on the test set
3. Using the single model generated in step 2. for cross predictions
4. Using the single model generated in step 2. to predict the energies of the optimised structures

For all of the above tasks, there is a script for the VR-NN (scripts ending with 'vr') and the MD-NN (scripts ending with 'md').

The scripts to generate the learning curves can be run independently and will generate a `.npz` file with the results.

Script 2 needs to be run before 3 and 4.  
