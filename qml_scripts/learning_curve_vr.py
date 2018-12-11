"""
This script generates a learning curve for the model trained on the VR data.
"""

from qml.aglaia.aglaia import ARMP
import numpy as np
import h5py
from sklearn import model_selection as modsel
import tensorflow as tf
import os

# Getting the dataset
cwd = os.path.dirname(os.path.realpath(__file__))
data = h5py.File(cwd + "../data_sets/isopentane_cn_vr_pbe.hdf5", "r")

xyz_isopent = np.array(data.get("xyz"))
ene_isopent = np.array(data.get("ene"))*2625.50
ref_ene = -290.175 * 2625.50
ene_isopent = ene_isopent - ref_ene
zs_isopent = np.array(data.get("zs"), dtype=np.int32)
traj_idx = np.array(data.get("traj_idx"))
file_idx = np.array(data.get("Filenumber"))

# Finding the indices of the last trajectory so that it can be used as a test set
idx_test = np.where(traj_idx == 22)[0]
idx_train = np.where(traj_idx != 22)[0]
np.random.shuffle(idx_train)

tot_samples_train = xyz_isopent[idx_train].shape[0]
n_samples = [100, 300, 1000, 3000, 10000, tot_samples_train]

scores = []
traj_scores = []

# Creating the estimator
acsf_params = {"nRs2":14, "nRs3":14, "nTs":14, "rcut":3.29, "acut":3.29, "zeta":100.06564927139748, "eta":39.81824764370754}
estimator = ARMP(iterations=2633, batch_size=22, l1_reg=1.46e-05, l2_reg=0.0001, learning_rate=0.0013, representation_name='acsf',
                 representation_params=acsf_params, tensorboard=True, store_frequency=25, hidden_layer_sizes=(185,))

estimator.set_properties(ene_isopent)
estimator.generate_representation(xyz_isopent, zs_isopent, method="fortran")

# Training the model on 3 folds of n data points
for n in n_samples:

    cv_idx = idx_train[:n]
    splitter = modsel.KFold(n_splits=3, random_state=42, shuffle=True)
    indices = splitter.split(cv_idx)

    scores_per_fold = []
    traj_scores_per_fold = []

    for item in indices:
        idx_train_fold = cv_idx[item[0]]
        idx_test_fold = cv_idx[item[1]]

        estimator.fit(idx_train_fold)

        score = estimator.score(idx_test_fold)
        traj_score = estimator.score(idx_test)
        scores_per_fold.append(score)
        traj_scores_per_fold.append(traj_score)

        tf.reset_default_graph()

    scores.append(scores_per_fold)
    traj_scores.append(traj_scores_per_fold)

# Saving the data to an .npz file
np.savez("./plot/scores_vr.npz", np.asarray(n_samples), np.asarray(scores), np.asarray(traj_scores))

