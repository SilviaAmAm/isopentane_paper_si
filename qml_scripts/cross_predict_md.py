"""
This script uses the model trained in the script `production_model_md.py` to predict the energies of the structures contained in the data set `isopentane_cn_vr_pbe.hdf5`.
"""


from qml.aglaia.aglaia import ARMP
import numpy as np
import h5py
import tensorflow as tf
from random import shuffle
import os

# Getting the iMD-VR dataset
cwd = os.path.dirname(os.path.realpath(__file__))
data = h5py.File(cwd + "../data_sets/isopentane_cn_vr_pbe.hdf5", "r")

xyz_isopent = np.array(data.get("xyz"))
ene_isopent = np.array(data.get("ene"))*2625.50
ref_ene = -290.175 * 2625.50
ene_isopent = ene_isopent - ref_ene
zs_isopent = np.array(data["zs"], dtype=np.int32)

# Shuffling the indices of the data and then selecting the first 9625 data points
idx = list(range(len(ene_isopent)))
shuffle(idx)
idx = idx[:9625]

# Appending the true energies to a list
predictions = [ene_isopent[idx]]

# Creating the estimator
acsf_params = {"nRs2":10, "nRs3":10, "nTs":10, "rcut":3.18, "acut":3.18, "zeta":52.779232035094125, "eta":1.4954812022150898}

estimator = ARMP(iterations=5283, batch_size=37, l1_reg=8.931599068573057e-06, l2_reg=3.535679697949907e-05, learning_rate=0.0008170485394812195, representation_name='acsf', representation_params=acsf_params, tensorboard=True, store_frequency=25, hidden_layer_sizes=(15,88))

# Putting the data into the model
estimator.set_properties(ene_isopent)
estimator.generate_representation(xyz_isopent, zs_isopent, method="fortran")
estimator.load_nn("md-nn")

# Predicting the energies
predictions.append(estimator.predict(idx))

# Scoring the results
score = estimator.score(idx)
print(score)

# Saving the predictions to a npz file
np.savez("cross_pred_md_on_vr.npz", np.asarray(predictions))

