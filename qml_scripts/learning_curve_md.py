"""
This script generates a learning curve for the the model trained on the constrained MD data set.
"""

from qml.aglaia.aglaia import ARMP
import numpy as np
import h5py
from sklearn import model_selection as modsel
import tensorflow as tf
import os

# Getting the dataset
cwd = os.path.dirname(os.path.realpath(__file__))
data = h5py.File(cwd + "/../data_sets/isopentane_cn_vr_pbe.hdf5", "r")

xyz_isopent = np.array(data.get("xyz"))
ene_isopent = np.array(data.get("ene"))*2625.50
ref_ene = -290.175 * 2625.50
ene_isopent = ene_isopent - ref_ene
zs_isopent = np.array(data.get("zs"), dtype=np.int32)
h_id = np.array(data.get("h_id"))

# Finding the indices to use as a test
idx_test = np.where(h_id == 2)[0]
idx_train = np.where(h_id != 2)[0]
np.random.shuffle(idx_train)

tot_samples_train = xyz_isopent[idx_train].shape[0]
n_samples = [100, 300, 1000, 3000, tot_samples_train]

scores = []
traj_scores = []

# Creating the estimator
acsf_params = {"nRs2":10, "nRs3":10, "nTs":10, "rcut":3.18, "acut":3.18, "zeta":52.779232035094125, "eta":1.4954812022150898}
estimator = ARMP(iterations=5283, batch_size=37, l1_reg=8.931599068573057e-06, l2_reg=3.535679697949907e-05,
                 learning_rate=0.0008170485394812195, representation_name='acsf', representation_params=acsf_params,
                 tensorboard=True, store_frequency=25, hidden_layer_sizes=(15,88))

estimator.set_properties(ene_isopent)
estimator.generate_representation(xyz_isopent, zs_isopent, method="fortran")

# Training the model on 3 folds of n samples
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

        # Scoring the model
        score = estimator.score(idx_test_fold)
        traj_score = estimator.score(idx_test)
        scores_per_fold.append(score)
        traj_scores_per_fold.append(traj_score)

        tf.reset_default_graph()

    scores.append(scores_per_fold)
    traj_scores.append(traj_scores_per_fold)

# Saving the results to a .npz file
np.savez("./plot/scores_md.npz", np.asarray(n_samples), np.asarray(scores), np.asarray(traj_scores))

