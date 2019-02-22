# Hyper-parameter optimization with Osprey

This folder contains all scripts to reproduce the hyper-parameter optimization. We used a custom fork of osprey, available [here](https://github.com/larsbratholm/osprey). The commit used was `4bfbb14`.

## Creating a model for use with osprey

[make_model_pickle.py](./make_model.pickle.py) Creates the input needed for Osprey. 
The dataset is loaded and turned into a QML data object.
A sklearn pipeline is created that first creates the Atom-centered symmetry functions, then passes them to the neural network.
The data object is stored in the pipeline. By doing this, we can pass e.g. `[0,1,2]` to the fit function to fit a model to the first three data points, without having to pass coordinates, nuclear charges and energies every time.
The model is stored as a pickle named `model.pickle`.
A file named `idx.csv` is created that has all the indices available in the data object.
If we have `n` data points, `idx.csv` will contain the numbers between `0` and `n-1`.
Finally a file named `groups.csv` that contains information on which trajectory each data points is from.
This makes us able to not mix trajectories in the train/validation splits in Osprey, by using the GroupKFold cross-validator.

## Running Osprey

The parameter space to explore and the method and model to use is defined in the yaml config files. [config1a.yaml](./config1a.yaml) shows an input file that uses the EI acquisition function to explore the parameters of a neural network with a single hidden layer, while [config1b.yaml](./config1b.yaml) uses UCB.
An Osprey worker can be run with `osprey worker -n <number of steps> <yaml file>`. Multiple workers can be run in parallel.
