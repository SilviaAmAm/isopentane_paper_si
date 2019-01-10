# Supporting Information

This repository contains all the scripts that were used to generate the data reported in the paper XXX.
It contains 4 folders:

1. [molpro](./molpro): Input files to Molpro for running the constrained optimizations and single point energies and forces.

2. [constrained_md](./constrained_md): Input files to CP2K for running the constrained MD.

3. [data_sets](./data_sets): All the data sets that were used for the generation of the results in the paper.

4. [qml_scripts](./qml_scripts): All the scripts used to fit the neural networks that recreate the results in the paper.


## Instructions for QML installation

Go to the [QML repository](https://github.com/qmlcode/qml) and clone it:

```
git clone https://github.com/qmlcode/qml.git
cd qml
```

Then, check out the version that has been used to produce the results in the paper:

```
git checkout develop
git checkout 2b462070de3532a3e6d2487a7f138df9f8d84c06
```

Now that the right version has been checked out, you can install it:

```
python install setup.py
```

## Other packages needed

In order to run the scripts, you will also need to install:

1. TensorFlow or tensorflow-gpu (>= 1.9)
2. H5py
3. Matplotlib
4. Seaborn

## What does NarupaXR look like?

You can view a video of the NarupaXR in action [here](https://vimeo.com/310557619).

 ![Image](visuals/narupaxr.png?raw=true)
