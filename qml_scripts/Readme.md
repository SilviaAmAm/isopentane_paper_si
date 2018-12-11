# General Scripts

This folder contains the scripts used to calculate the results of the paper. It contains 4 types of scripts:

1. Generation of learning curves
2. Training of a single model and predicting on the test set
3. Using the single model generated in step 2. for cross predictions
4. Using the single model generated in step 2. to predict the energies of the optimised structures

For all of the above tasks, there is a script for the VR-NN (scripts ending with 'vr') and the MD-NN (scripts ending with 'md').

## Generating the learning curves

The scripts to generate the learning curves (`learning_curve_md.py` and
`learning_curve_vr.py`) can be run independently and will generate a `.npz` file with the results.
Once both scripts have been run, the results can be plotted using the script `plot_learning_curve.py` in the folder `plot`.

## Training a single model

A VR-NN can be trained using script `production_model_vr.py`, while a MD-NN can be trained using the script `production_model_md.py`.

These will save a trained model and print the score of that model on the test set.

## Predictions

Once a VR-NN and a MD-NN have been trained, they can be used for predictions. The script `cross_predict_vr.py` can be used to use the VR-NN to predict the energies of the structures in the constrained MD data set. On the other hand, the script and `cross_predict_md.py` can be used to use the MD-NN to predict the energies of the structures in the VR data set.

The scripts `surface_predictions_vr.py` and `surface_predictions_md.py` use the VR-NN and the MD-NN respectively to predict the energies of the optimised structures. The results can be plotted using the script `plot_predicted_surface.py` in the folder `plot`.