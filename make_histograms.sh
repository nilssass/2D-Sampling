#!/bin/bash

FILE_INPUT="/Users/nils/smash-vhlle-hybrid/build/Hybrid_Results/RuRu_200.0/1/Sampler/particle_lists.oscar"
DIRECTORY_OUTPUT="/Users/nils/Python_Scripts/Freezeout_Restore_3D"

# Setting Binning Parameters

hist_min=-5.0
hist_max=5.0
num_bins=60

python3 y_eta_spectra.py ${hist_min} ${hist_max} ${num_bins} ${FILE_INPUT} ${DIRECTORY_OUTPUT}
