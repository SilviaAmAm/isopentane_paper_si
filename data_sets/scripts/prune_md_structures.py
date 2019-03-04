import numpy as np
import h5py

data = h5py.File("../isopentane_cn_md_pbe.hdf5", "r")

xyz = np.asarray(data.get("xyz"))
ene = np.asarray(data.get("ene"))
zs = np.asarray(data.get("zs"), dtype=np.int32)
snapshot_idx= np.asarray(data.get("snapshot_idx"))
ch_dist_cn = np.asarray(data.get("ch_dist_cn"))
ch_dist_alk = np.asarray(data.get("ch_dist_alk"))
h_id = np.asarray(data.get("h_id"))


h_mask = (zs[0] == 1)
c_mask = (zs[0] == 6)

# Remove structures where the cyanide C and N are further
# than 1.5 angstrom apart
cn_distances = np.sum((xyz[:,17] - xyz[:,18])**2, axis=1)**0.5
cn_mask = (cn_distances < 1.5)

# Remove structures where two hydrogens are closer
# than 1.5 angstrom apart
hh_distances = np.sum((xyz[:,h_mask,None] - xyz[:,None,h_mask])**2, axis=3)**0.5
hh_distances += np.eye(h_mask.sum()) * 10
# Change to 0.9 to remove only free H2, and not local minima
hh_mask = (hh_distances > 1.5).all((1,2))

ch_pairs = [(13,14), (13,15), (13,16), (6,12), (6,11),
            (1,7), (5,8), (5,9), (5,10), (0,2), (0,3), 
            (0,4)]

mask = cn_mask * hh_mask

# Remove structures where the CH distances
# are more than 1.4 angstrom between H and C
# that should be covalently bonded
for c_idx, h_idx in ch_pairs:
    ch_distances = np.sum((xyz[:,c_idx] - xyz[:,h_idx])**2, axis=1)**0.5
    ch_mask = (ch_distances < 1.4)
    # Ignore the constrained hydrogens
    ch_mask[h_id == h_idx] = True
    mask *= ch_mask

print(sum(mask), "remaining structures out of", len(mask))

xyz = xyz[mask]
ene = ene[mask]
zs = zs[mask]
snapshot_idx = snapshot_idx[mask]
ch_dist_cn = ch_dist_cn[mask]
ch_dist_alk = ch_dist_alk[mask]
h_id = h_id[mask]


f = h5py.File("cn_isopentane_md_new.hdf5", "w")

f.create_dataset("h_id", h_id.shape, data=h_id)
f.create_dataset("ch_dist_alk", ch_dist_alk.shape, data=ch_dist_alk)
f.create_dataset("ch_dist_cn", ch_dist_cn.shape, data=ch_dist_cn)
f.create_dataset("snapshot_idx", snapshot_idx.shape, data=snapshot_idx)
f.create_dataset("xyz", xyz.shape, data=xyz)
f.create_dataset("ene", ene.shape, data=ene)
f.create_dataset("zs", zs.shape, data=zs)
f.close()

#idx = failed[0][1]
#print(xyz[idx][0], h_id[idx])
#hh_mask = (hh_distances > 0.8).all((1,2))
#hh_mask2 = (hh_distances > 0.9).all((1,2))
#print(sum(hh_mask))
#print(sum(hh_mask2))
#idx = np.where(hh_mask * ~hh_mask2)[0][0]
#print(xyz[idx][0], h_id[idx])
#idx = np.where(hh_mask * ~hh_mask2)[0][1]
#print(xyz[idx][0], h_id[idx])
#idx = np.where(hh_mask * ~hh_mask2)[0][2]
#print(xyz[idx][0], h_id[idx])
#quit()
