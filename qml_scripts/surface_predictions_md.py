"""
This script uses the model that was trained on the data sampled with the constrained MD to predict the dft energies of the surface.
"""

from qml.aglaia.aglaia import ARMP
import numpy as np
import h5py
import time
import os

# Getting the dataset
cwd = os.path.dirname(os.path.realpath(__file__))
data = h5py.File(cwd + "/../data_sets/isopentane_cn_vr_pbe.hdf5", "r")

ene_surface = np.array(data.get("ene"))
xyz_surface = np.array(data.get("xyz"))
zs_surface = np.array(data.get("zs"))
ch_dist_alk = np.array(data.get("ch_dist_alk"))
ch_dist_cn = np.array(data.get("ch_dist_cn"))
h_id = np.array(data.get("h_id"))

n_samples = xyz_surface.shape[0]

# Creating the estimator
acsf_params = {"nRs2":10, "nRs3":10, "nTs":10, "rcut":3.18, "acut":3.18, "zeta":52.779232035094125, "eta":1.4954812022150898}

estimator = ARMP(iterations=5283, batch_size=37, l1_reg=8.931599068573057e-06, l2_reg=3.535679697949907e-05, learning_rate=0.0008170485394812195, representation_name='acsf', representation_params=acsf_params, tensorboard=True, store_frequency=25, hidden_layer_sizes=(15,88))

# Loading the model previously trained
estimator.load_nn("md-nn")
estimator.set_properties(ene_surface)

# Generating the representation
start = time.time()
estimator.generate_representation(xyz_surface, zs_surface, method="fortran")
end = time.time()
print("The time taken to generate the representations is %s s" % (str(end-start)))
print("The shape of the representations is %s" % (str(estimator.representation.shape)))

# Predicting the energies
idx = list(range(n_samples))
predictions = estimator.predict(idx)

# Saving the results to a hdf5 file
f = h5py.File("MD-NN_surface_predictions.hdf5", "w")
f.create_dataset("ch_dist_alk", ch_dist_alk.shape, data=ch_dist_alk)
f.create_dataset("ch_dist_cn", ch_dist_cn.shape, data=ch_dist_cn)
f.create_dataset("h_id", h_id.shape, data=h_id)
f.create_dataset("xyz", xyz_surface.shape, data=xyz_surface)
f.create_dataset("ene", predictions.shape, data=predictions)
f.create_dataset("zs", zs_surface.shape, data=zs_surface)
f.close()
