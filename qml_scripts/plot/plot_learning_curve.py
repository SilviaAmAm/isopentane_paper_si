"""
This script plots the learning curve using the data generated by the scripts `learning_curve_md.py` and
`learning_curve_vr.py`
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
sns.set_style("white")

# Extracts the VR data from the .npz file
data_vr = np.load("scores_vr.npz")
n_samples_vr = data_vr["arr_0"]         # Total number of samples before CV splitting
scores_vr = data_vr["arr_1"]            # Scores on the dev set
traj_scores_vr = data_vr["arr_2"]       # Scores on the test set

# Calculating the mean score and its std for each set of scores
mean_scores_vr = []
err_scores_vr = []
mean_traj_scores_vr = []
err_traj_scores_vr = []

for item in scores_vr:
    mean_scores_vr.append(-np.mean(item))
    err_scores_vr.append(np.std(item,ddof=1))
for item in traj_scores_vr:
    mean_traj_scores_vr.append(-np.mean(item))
    err_traj_scores_vr.append(np.std(item, ddof=1))

mean_scores_vr = np.asarray(mean_scores_vr)
err_scores_vr = np.asarray(err_scores_vr)
mean_traj_scores_vr = np.asarray(mean_traj_scores_vr)
err_traj_scores_vr = np.asarray(err_traj_scores_vr)

# Extracts the MD data from the .npz file
data_md = np.load("scores_md.npz")
n_samples_md = data_md["arr_0"]
scores_md = data_md["arr_1"]
traj_scores_md = data_md["arr_2"]

# Calculating the mean score and its std for each set of scores
mean_scores_md = []
err_scores_md = []
mean_traj_scores_md = []
err_traj_scores_md = []

for item in scores_md:
    mean_scores_md.append(-np.mean(item))
    err_scores_md.append(np.std(item))
for item in traj_scores_md:
    mean_traj_scores_md.append(-np.mean(item))
    err_traj_scores_md.append(np.std(item))

mean_scores_md = np.asarray(mean_scores_md)
err_scores_md = np.asarray(err_scores_md)
mean_traj_scores_md = np.asarray(mean_traj_scores_md)
err_traj_scores_md = np.asarray(err_traj_scores_md)

# Plotting the test set scores as a function of number of samples
plt.figure(figsize=(10,8))
plt.plot(n_samples_md, mean_traj_scores_md, label="MD test set")
plt.fill_between(n_samples_md, mean_traj_scores_md - err_traj_scores_md, mean_traj_scores_md + err_traj_scores_md, alpha=0.4)
plt.plot(n_samples_vr, mean_traj_scores_vr, label="VR test set")
plt.fill_between(n_samples_vr, mean_traj_scores_vr - err_traj_scores_vr, mean_traj_scores_vr + err_traj_scores_vr, alpha=0.4)

plt.xlabel("Number of training samples", fontsize=15)
plt.ylabel("MAE (kJ/mol)", fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.legend()
plt.yscale("log")
plt.xscale("log")
plt.savefig("learning_curve_vr_md_log.png", dpi=200)
plt.show()