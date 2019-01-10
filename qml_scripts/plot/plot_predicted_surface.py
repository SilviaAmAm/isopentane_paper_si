import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
sns.set_style("white")
import h5py
import os


# Reference Energy in kJ/mol
ene_ref = -290.175 * 2625.50

# Surface Data
# # Uncomment this to plot the DFT surface (Energy units: Hartree)
# data = h5py.File(os.path.dirname(os.path.realpath(__file__)) + "../data_sets/isopentane_cn_surface_pbe.hdf5", "r")
# # Uncomment this to plot the VR-NN predicted surface (Energy units: kJ/mol)
data = h5py.File("VR-NN_surface_predictions.hdf5", "r")
# # Uncomment this to plot the MD-NN predicted surface (Energy units: kJ/mol)
# data = h5py.File("MD-NN_surface_predictions.hdf5", "r")

# Extracting the data (If plotting the DFT surface, uncomment unit conversion!)
xyz = np.array(data.get("xyz"))
# ene = np.array(data.get("ene"))*2625.5 - ene_ref        # Converting the energy to kJ/mol and removing the reference energy
ene = np.array(data.get("ene"))
zs = np.array(data.get("zs"))
ch_dist_alk = np.array(data.get("ch_dist_alk"))
ch_dist_cn = np.array(data.get("ch_dist_cn"))
h_id = np.array(data.get("h_id"))

# Idx of the Hydrogen for which to plot the surface (Chose 7 for a primary, 10 for a secondary and 11 for a tertiary H)
idx = 7

# Making a single array with the ch distances
uniq = np.unique(np.concatenate([ch_dist_alk,ch_dist_cn]))

# Look up table to convert a distance to the index in the grid
value_to_index = {}
for i, v in enumerate(uniq):
    value_to_index[v] = i

# create grids
X,Y = np.meshgrid(uniq,uniq)

# Make an array. Could probably use a float np.array with np.nan instead of None
Z = [[None for i in range(uniq.size)] for j in range(uniq.size)]

# Fill the array
for sample_idx in range(len(ene)):
    if h_id[sample_idx] != idx:
        continue

    if ch_dist_alk[sample_idx] > 1.75 and ch_dist_cn[sample_idx] > 1.8:
        continue

    a = ch_dist_alk[sample_idx]
    b = ch_dist_cn[sample_idx]
    c = ene[sample_idx]

    if a not in value_to_index or b not in value_to_index:
        continue
    i = value_to_index[a]
    j = value_to_index[b]
    Z[i][j] = c

# Plot the contour
plt.contourf(Y,X,Z,np.arange(-200, 150, 20), cmap="Blues_r")
plt.xlabel("D2 (Å)")
plt.ylabel("D1 (Å)")
cbar = plt.colorbar()
cbar.ax.set_ylabel('Energy (kJ/mol)', labelpad=+2)
# plt.savefig("VR_surface.png", dpi=200)
plt.show()