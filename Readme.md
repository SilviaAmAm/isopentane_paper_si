# Supporting Information

This repository contains all the scripts that were used to generate the data reported in the paper XXX.
It contains 3 folders:

1. Data sets: folder `data_sets` contains all the data sets that were used for the generation of the results in the paper.

2. Generating the results: folder `qml_scripts` contains all the scripts used to generate the results.

## Instructions for QML installation

Go to [this fork](https://github.com/SilviaAmAm/qml) of the QML repository and clone it:

```
git clone https://github.com/SilviaAmAm/qml.git
cd qml
```

Then, check out the version that has been used to produce the results in the paper:

```
git checkout develop
git checkout e2feecfb559073c79647fec9039c97fd2e2232e9
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

You can view a video of the NarupaXR in action [here](https://www.youtube.com/watch?v=oUdHrNsiXlA).

 ![Image](visuals/narupaxr.png?raw=true)
