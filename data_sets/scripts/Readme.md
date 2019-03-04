# Data set scripts

This folder contains some utility scripts related to the data sets:

1. `prune_vr_structures.py`
2. `prune_md_structures.py`
3. `hdf5_to_xyz.py        `

## 1. Pruning VR trajectories

The `prune_vr_structures.py` script is simple. 1200 snapshots is given for each VR trajectory, but only the middle 1000 is used in the paper.

## 2. Constrained MD sampled data

This is the data obtained from sampling the potential energy surface with constrained MD (using PM6). The energies have been recalculated using CF-uPBE with TZVP basis set. The energies are in Hartrees. The data from this data set can be extracted as follows: 

```
import numpy as np
import h5py

data = h5py.File("isopentane_cn_md_pbe.hdf5", "r")

xyz = np.array(data.get("xyz"))
ene = np.array(data.get("ene"))
forces = np.array(data.get("forces"))
zs = np.array(data.get("zs"), dtype=np.int32)
snapshot_idx= np.array(data.get("snapshot_idx"))
ch_dist_cn = np.array(data.get("ch_dist_cn"))
ch_dist_alk = np.array(data.get("ch_dist_alk"))
h_id = np.array(data.get("h_id"))
```

Where `xyz`, `ene`, `forces` and `zs` are the same as in the previous data set. The different things are `h_id` which is an array of shape `(n_samples,)` containing the index of the H being constrained, `snapshot_idx` is an array of shape `(n_samples,)` containing the index of the frame within a constrained MD run, `ch_dist_alk` and `ch_dist_cn` are arrays of shape `(n_samples,)` containing the distance between the H and the carbon on the alkane and the carbon on the cyano radical respectively.

## 3. Surface with optimised structures 

This data set contains the optimised structures that make up the surface (Fig. 10 in the paper). The data can be extracted in the same way as for the `isopentane_cn_md_pbe.hdf5` data set.
