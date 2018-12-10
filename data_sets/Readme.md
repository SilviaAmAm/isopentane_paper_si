# Data sets

This folder contains all of the data sets used in the paper:

1. `isopentane_cn_vr_pbe.hdf5`
2. `isopentane_cn_md_pbe.hdf5` 
3. `isopentane_cn_surface_pbe.hdf5`

## VR sampled data 

This is the data obtained from sampling the potential energy surface with the VR (using PM6). The energies have been recalculated using CF-uPBE with TZVP basis set. The energies are in Hartrees. The data from this data set can be extracted as follows:

```
import numpy as np
import h5py

data = h5py.File("isopentane_cn_vr_pbe.hdf5", "r")

xyz = np.array(data.get("xyz"))
ene = np.array(data.get("ene"))
forces = np.array(data.get("forces"))
zs = np.array(data.get("zs"), dtype=np.int32)
traj_idx = np.array(data.get("traj_idx"))
file_idx = np.array(data.get("Filenumber"))
```

Where `xyz` is an array of shape `(n_samples, n_atoms, 3)` containing the Cartesian coordinates, `ene` is an array of shape `(n_samples,)` containing the energies in Hartree, `forces` is an array of shape `(n_samples, n_atoms, 3)` containing the forces acting on each atom, `zs` is an array of shape `(n_samples, n_atoms)` containing the nuclear charge of each atom, `traj_idx` is an array of shape `(n_samples,)` containing the index of the trajectory from which that structure came from, `file_idx` is an array of shape `(n_samples,)` containing the index of a structure within a particular trajectory.

## Constrained MD sampled data

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

## Surface with optimised structures 

This data set contains the optimised structures that make up the surface (Fig. 10 in the paper). The data can be extracted in the same way as for the `isopentane_cn_md_pbe.hdf5` data set.
