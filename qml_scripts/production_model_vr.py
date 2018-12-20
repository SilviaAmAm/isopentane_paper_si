"""
This script trains a model on 9625 data points of the data set sampled using VR.
"""

from qml.aglaia.aglaia import ARMP
import numpy as np
import h5py
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
from sklearn import model_selection as modsel
import tensorflow as tf
import time
from random import shuffle
import os

# Getting the dataset
cwd = os.path.dirname(os.path.realpath(__file__))
data = h5py.File(cwd + "/../data_sets/isopentane_cn_vr_pbe.hdf5", "r")

xyz_isopent = np.array(data.get("xyz"))
ene_isopent = np.array(data.get("ene"))*2625.50
ref_ene = -290.175 * 2625.50
ene_isopent = ene_isopent - ref_ene
zs_isopent = np.array(data.get("zs"), dtype=np.int32)
traj_idx = np.array(data.get("traj_idx"))
file_idx = np.array(data.get("Filenumber"))

# Finding the indices of the last trajectory so that it can be used as a test set
idx_test = np.where(traj_idx==22)[0]
idx_train = np.where(traj_idx!=22)[0]
shuffle(idx_train)

# Making sure that the model is trained on the same number of samples as the MD-NN
idx_train_half = idx_train[:9625]

# Creating the estimator
acsf_params = {"nRs2":14, "nRs3":14, "nTs":14, "rcut":3.29, "acut":3.29, "zeta":100.06564927139748, "eta":39.81824764370754}
estimator = ARMP(iterations=2633, batch_size=22, l1_reg=1.46e-05, l2_reg=0.0001, learning_rate=0.0013, representation_name='acsf',
                 representation_params=acsf_params, tensorboard=True, store_frequency=25, hidden_layer_sizes=(185,))

estimator.set_properties(ene_isopent)
estimator.generate_representation(xyz_isopent, zs_isopent, method="fortran")

# Fitting the estimator and scoring it
estimator.fit(idx_train_half)
score = estimator.score(idx_test)

# Saving the model for later reuse
model_name = "vr-nn"
estimator.save_nn(model_name)

print(score)
