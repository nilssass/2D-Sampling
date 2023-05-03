This is  a collection of scripts I am using to analyze my data and plot my results

### 2D Sampler Code
The sampler code for the 2d setup can be found on the branch `nsass/sampler_2D`
of the repository \
[https://github.com/smash-transport/smash-hadron-sampler/tree/master](https://github.com/smash-transport/smash-hadron-sampler/tree/master)

### Creating Rapidity and Spacetime Rapidity Spectra
From the .oscar output of the sampler the dN/dy and dN/dEta spectra can be created with the bash script `make_histograms.sh` which automatically calls the `y_eta_spectra.py` script with 5 arguments as
```
python3 [path_to_script]/y_eta_spectra.py hist_min hist_max num_bins PATH_OSCAR PATH_OUTPUT
```
where
```
hist_min:       lower limit for histogram (make sure that all particles are contained, I use -5.0)
hist_max:       upper limit for histogram (                                                   5.0)
num_bins:       number of bins
PATH_OSCAR:     path to .oscar output from sampler
PATH_OUTPUT:    path to output directory
```
These parameters can be set in the bash script. Executing the bash script by `bash make_histograms.sh` will create to files `dNdy.txt` and `dNdEta.txt` containing the corresponding histograms.

### Plotting the Histograms
Save the python script `plot_histograms.py` in the same directory as the histogram .txt files and run
```
python3 plot_histograms.py
```
This will create the plots for the corresponding histograms. In order to change the particles plotted, one can change the pdg codes inthe plotting script in line 189 (and 192)
