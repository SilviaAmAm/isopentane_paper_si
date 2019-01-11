# MIT License
#
# Copyright (c) 2018 Silvia Amabilino
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import pickle
import numpy as np
import sklearn.pipeline
from qml import qmlearn
import h5py

# Create data
dataset = h5py.File("../data_sets/pbe_isopentane_cn_vr_pbe.hdf5")
data = qmlearn.Data()
traj_idx = np.asarray(dataset['traj_idx'], dtype=int)
# Keep trajectory 22 as a test set
mask = (traj_idx == 22)
data.coordinates = np.asarray(dataset['xyz'])[~mask]
data.nuclear_charges = np.array(dataset['zs'])[~mask]
data._set_ncompounds(len(data.nuclear_charges))
data.natoms = np.asarray([len(data.nuclear_charges[0])]*len(data.nuclear_charges))
energies = np.asarray(dataset['ene'])[~mask]*2625.50
energies -= np.mean(energies)
data.set_energies(energies)

# Create model
estimator = sklearn.pipeline.make_pipeline(
                qmlearn.representations.AtomCenteredSymmetryFunctions(data),
                qmlearn.models.NeuralNetwork(hl2=0, hl3=0, iterations=50)
                )


pickle.dump(estimator, open('model.pickle', 'wb'))
indices = np.arange(len(data.coordinates))
with open('idx.csv', 'w') as f:
    for i in indices:
        f.write('%s\n' % i)
indices = traj_idx[~mask]
with open('groups.csv', 'w') as f:
    for i in indices:
        f.write('%s\n' % i)
