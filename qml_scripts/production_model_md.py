from qml.aglaia.aglaia import ARMP
import numpy as np
import h5py
from random import shuffle

# Getting the dataset
data = h5py.File("/home/sa16246/data_sets/cn_reactions/constrained_md/cn_isopentane_md_without_exploded.hdf5", "r")

xyz_isopent = np.array(data.get("xyz"))
ene_isopent = np.array(data.get("ene"))*2625.50
ref_ene = -290.175 * 2625.50
ene_isopent = ene_isopent - ref_ene
zs_isopent = np.array(data.get("zs"), dtype=np.int32)
h_id = np.array(data.get("h_id"))

# Finding the indices of the last trajectory so that it can be used as a test set
idx_test = np.where(h_id == 2)
idx_train = np.where(h_id != 2)
shuffle(idx_train)

# Making sure that the model is trained on the same number of samples as the constrained MD
idx_train_half = idx_train[:10350]

acsf_params = {"nRs2":10, "nRs3":10, "nTs":10, "rcut":3.18, "acut":3.18, "zeta":52.779232035094125, "eta":1.4954812022150898}

# Creating the estimator
estimator = ARMP(iterations=5283, batch_size=37, l1_reg=8.931599068573057e-06, l2_reg=3.535679697949907e-05, learning_rate=0.0008170485394812195, representation_name='acsf', representation_params=acsf_params, tensorboard=True, store_frequency=25, hidden_layer_sizes=(15,88))

estimator.set_properties(ene_isopent)
estimator.generate_representation(xyz_isopent, zs_isopent, method="fortran")

estimator.fit(idx_train_half)
score = estimator.score(idx_test)

model_name = "md-nn"
estimator.save_nn(model_name)

print(score)