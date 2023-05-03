import numpy as np
from matplotlib import pyplot as plt

def load(fname):
    data = []
    with open(fname, 'r') as f:
        for line in f.readlines():
            data_line = line.replace('\n','').split(' ')
            data_line = [x for x in data_line if x != '']
            data.append(data_line)
    return data

def get_bin_positions(data):
    bin_positions = []
    for line in data:
        if line[0] == '#':
            continue
        else:
            bin_positions.append(line[0])
    return np.array(bin_positions, dtype=np.float32)
        
def get_data_header(data):
    header = data[1]
    return header[2:]

def get_histograms(data):
    num_particles = len(get_data_header(data))
    num_bins = len(get_bin_positions(data))
    hist = np.zeros((num_bins, num_particles))
    count = 0
    
    for line in data:
        if '#' in line:
            continue
        else:
            hist[count,:] = np.array(line[1:], dtype=np.float64)
            count += 1
    return hist

def pdg_to_particle_str(pdg_str):
    
    pdg_particle_list = {
        # Uses PDG code as keys 
        '2212'  : r'$p$' ,             # Proton
        '-2212' : r'$\bar{p}$',        # Anti proton
        '111'   : r'$\pi^0$',          # Pi0
        '211'   : r'$\pi^+$',          # Pi+
        '-211'  : r'$\pi^-$',          # Pi-
        '321'   : r'$K^+$',            # K+
        '-321'  : r'$K^-$',            # K-
        '3122'  : r'$\Lambda$',        # Lambda
        '-3122' : r'$\bar{\Lambda}$',  # Anti lambda
        }
    return pdg_particle_list[pdg_str]

#   From ChatGpt:
#    
#   def plot(data, pdg, OUTPUT_FILE=False, figsize=(10, 6)):
#     """
#     Plot histogram for given PDG code or list/tuple of PDG codes from data.
    
#     Args:
#         data (numpy.ndarray): Data array containing histograms.
#         pdg (str, list, tuple): PDG code or list/tuple of PDG codes to plot.
#         OUTPUT_FILE (str, optional): File name to save the plot. Default is False.
#         figsize (tuple, optional): Figure size as (width, height). Default is (10, 6).
#     """
    
#     if isinstance(pdg, (str, list, tuple)):
#         if isinstance(pdg, str):
#             pdg = [pdg]
#         elif isinstance(pdg, (list, tuple)):
#             if not all(isinstance(item, str) for item in pdg):
#                 raise ValueError("PDG codes must be strings.")
        
#         header = get_data_header(data)
#         bins = get_bin_positions(data)
#         hist = get_histograms(data)
#         colors = get_colors(pdg)
        
#         plt.figure(figsize=figsize)
#         for particle, color in zip(pdg, colors):
#             particle_index = header.index(particle)
#             error_index = particle_index + 1
            
#             hist_particle = hist[:, particle_index]
#             err_particle = hist[:, error_index]
             
#             particle_label = pdg_to_particle_str(particle)
#             plt.plot(bins, hist_particle, c=color, label=particle_label, linewidth=2.0)
#             plt.fill_between(bins, hist_particle-err_particle, hist_particle+err_particle, color=color, alpha=0.4)
            
#         plt.grid(True,alpha=0.4)
#         plt.legend()
        
#         # Save Plot
#         if OUTPUT_FILE == False:
#             plt.savefig('plot.png', dpi=300)
#         else:
#             plt.savefig(OUTPUT_FILE, dpi=300)
#     else:
#         raise ValueError("PDG code must be a string or a list/tuple of strings.")
        
        
# def get_colors(pdg):
#     """
#     Get colors for PDG codes.
    
#     Args:
#         pdg (list, tuple): List/tuple of PDG codes.
        
#     Returns:
#         list: List of colors.
#     """
#     colors = []
#     if len(pdg) <= 4:
#         colors = ["#0A3C62","#4F7772","#94B282","#D9ED92"]
#     elif len(pdg) <= 6:
        
        


def plot(data, pdg, OUTPUT_FILE=False):
    
    if isinstance(pdg, str):
        colors = "#0A3C62"
    elif isinstance(pdg, (tuple, list)) and len(pdg) <= 4:
        colors = ["#0A3C62","#4F7772","#94B282","#D9ED92"]
    elif isinstance(pdg, (tuple, list)) and len(pdg) <= 6:
        colors = ["#0A3C62","#335F6C","#5D8375","#86A67F","#B0CA88","#D9ED92"]
    else:
        colors = ["#0A3C62","#215067","#38636D","#4F7772","#668B77","#7D9E7D","#94B282","#ABC687","#C2D98D","#D9ED92"]
    
    if isinstance(pdg, str):
        header = get_data_header(data)
        particle_index = header.index(pdg)
        error_index = particle_index + 1
        
        bins = get_bin_positions(data)
        hist = get_histograms(data)[:, particle_index]
        err = get_histograms(data)[:, error_index]
        
        particle_label = pdg_to_particle_str(pdg)
        plt.plot(bins, hist, label=particle_label, linewidth=2.0)
        plt.fill_between(bins, hist-err, hist+err, color=colors, alpha=0.4)
        plt.grid(True,alpha=0.4)
        plt.legend()
        
        # Save Plot 
        if OUTPUT_FILE == False:
            plt.savefig('plot.png', dpi=300)
        else:
            plt.savefig(OUTPUT_FILE, dpi=300)
        
    elif isinstance(pdg, list) or isinstance(pdg, tuple):
        count_colors = 0
        for particle in pdg:
            header = get_data_header(data)
            particle_index = header.index(particle)
            error_index = particle_index + 1
            
            bins = get_bin_positions(data)
            hist = get_histograms(data)[:, particle_index]
            err = get_histograms(data)[:, error_index]

            color = colors[count_colors]
            count_colors+=1
            
            particle_label = pdg_to_particle_str(particle)
            plt.plot(bins, hist, c=color, label=particle_label, linewidth=2.0)
            plt.fill_between(bins, hist-err, hist+err, color=color, alpha=0.4)
            plt.grid(True,alpha=0.4)
            plt.legend()
        
        # Save Plot
        if OUTPUT_FILE == False:
            plt.savefig('plot.png', dpi=300)
        else:
            plt.savefig(OUTPUT_FILE, dpi=300)


############################## Definitions End ################################ 
    

FILE_INPUT_DNDY = "./dNdy.txt"
FILE_INPUT_DNDETA = "./dNdEta.txt"

dNdy = load(FILE_INPUT_DNDY)
plot(dNdy, ('111', '211', '-211'), './dNdy')

dNdEta = load(FILE_INPUT_DNDETA)
#plot(dNdEta, ('2212', '111', '211'), './dNdEta')
