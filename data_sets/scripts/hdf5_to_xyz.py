import numpy as np
import h5py

CHARGE_TO_NAME = {1: "H",
                  6: "C",
                  7: "N"}

def write_xyz_batch(xyz,zs,idx):
    counter = {}
    n = len(zs)
    for i in range(n):
        traj_idx = idx[i]
        if traj_idx not in counter: counter[traj_idx] = 0
        write_xyz(xyz[i], zs[i], traj_idx, counter[traj_idx])
        counter[traj_idx] += 1

def write_xyz(xyz, nuclear_charges, traj_idx, count):
    filename = "%d_%d.xyz" % (traj_idx, count)
    n = len(xyz)
    with open(filename, "w") as f:
        f.write("%d\n\n" % n)
        for i in range(n):
            charge = nuclear_charges[i]
            element = CHARGE_TO_NAME[charge]
            f.write("%s %.7f %.7f %.7f\n" % (element, *xyz[i]))




if __name__ == "__main__":
    
    data = h5py.File("../isopentane_cn_md_pbe.hdf5")
    idx = np.asarray(data.get("traj_idx"))
    zs = np.asarray(data.get("zs"))
    xyz = np.asarray(data.get("xyz"))
    
    write_xyz_batch(xyz,zs,idx)
