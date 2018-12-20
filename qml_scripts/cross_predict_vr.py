"""
This script uses the model trained in the script `production_model_vr.py` and uses it to predict the energies of the structures in the data set `isopentane_cn_md_pbe.hdf5`.
"""

from qml.aglaia.aglaia import ARMP
import numpy as np
import h5py
from random import shuffle
import os

# Getting the CMD dataset
cwd = os.path.dirname(os.path.realpath(__file__))
data = h5py.File(cwd + "/../data_sets/isopentane_cn_md_pbe.hdf5", "r")

xyz_isopent = np.array(data.get("xyz"))
ene_isopent = np.array(data.get("ene"))*2625.50
ref_ene = -290.175 * 2625.50
ene_isopent = ene_isopent - ref_ene
zs_isopent = np.array(data["zs"], dtype=np.int32)

# Shuffling the indices
idx = list(range(len(ene_isopent)))
shuffle(idx)

predictions = [ene_isopent[idx]]

# Creating the estimator
acsf_params = {"nRs2":14, "nRs3":14, "nTs":14, "rcut":3.29, "acut":3.29, "zeta":100.06564927139748, "eta":39.81824764370754}
estimator = ARMP(iterations=2633, batch_size=22, l1_reg=1.46e-05, l2_reg=0.0001, learning_rate=0.0013, representation_name='acsf',
                 representation_params=acsf_params, tensorboard=True, store_frequency=25, hidden_layer_sizes=(185,))

# Input the data into the model
estimator.set_properties(ene_isopent)
estimator.generate_representation(xyz_isopent, zs_isopent, method="fortran")
estimator.load_nn("vr-nn")

# Predicting the energies
predictions.append(estimator.predict(idx))

# Scoring the results
score = estimator.score(idx)
print(score)

# Saving the results to a .npz file
np.savez("cross_pred_vr_on_md.npz", np.asarray(predictions))

