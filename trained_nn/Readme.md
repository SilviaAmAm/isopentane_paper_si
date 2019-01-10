# Trained models

This directory contains the iMDVR-NN and the CMD saved model. These can be reloaded and used for prediction. To reload a model, after having created the estimator object use the `load_nn()` function.

```
acsf_params = {"nRs2":10, "nRs3":10, "nTs":10, "rcut":3.18, "acut":3.18, "zeta":52.779232035094125, "eta":1.4954812022150898}
estimator = ARMP(iterations=5283, batch_size=37, l1_reg=8.931599068573057e-06, l2_reg=3.535679697949907e-05, learning_rate=0.0008170485394812195, representation_name='acsf', representation_params=acsf_params, tensorboard=True, store_frequency=25, hidden_layer_sizes=(15,88))

estimator.load_nn("md-nn")
```

