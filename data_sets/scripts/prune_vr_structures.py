import numpy as np
import h5py

data = h5py.File("isopentane_cn_vr_pbe.hdf5", "r")

xyz = np.array(data.get("xyz"))
traj_idx= np.array(data.get("traj_idx"))
filenumber = np.array(data.get("Filenumber"))

# Adjust
mid = np.where((filenumber > 200) & (filenumber < 1000))[0]
print(len(mid))
