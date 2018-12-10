from qml.aglaia.aglaia import ARMP
import numpy as np
import h5py
import tensorflow as tf
from random import shuffle

# Getting the dataset
data = h5py.File("/home/sa16246/data_sets/cn_reactions/pm6_sampling/pbe_isopentane_cn_vr_no_hnc.hdf5", "r")

xyz_isopent = np.array(data.get("xyz"))
ene_isopent = np.array(data.get("ene"))*2625.50
ref_ene = -290.175 * 2625.50
ene_isopent = ene_isopent - ref_ene
zs_isopent = np.array(data["zs"], dtype=np.int32)

idx = list(range(len(ene_isopent)))
shuffle(idx)
idx = idx[:10350]

predictions = [ene_isopent[idx]]

# Creating the estimator
acsf_params = {"nRs2":10, "nRs3":10, "nTs":10, "rcut":3.18, "acut":3.18, "zeta":52.779232035094125, "eta":1.4954812022150898}

estimator = ARMP(iterations=5283, batch_size=37, l1_reg=8.931599068573057e-06, l2_reg=3.535679697949907e-05, learning_rate=0.0008170485394812195, representation_name='acsf', representation_params=acsf_params, tensorboard=True, store_frequency=25, hidden_layer_sizes=(15,88))

estimator.set_properties(ene_isopent)
estimator.generate_representation(xyz_isopent, zs_isopent, method="fortran")
estimator.load_nn("md-nn")

predictions.append(estimator.predict(idx))

score = estimator.score(idx)
print(score)

np.savez("cross_pred_md_on_vr.npz", np.asarray(predictions))

