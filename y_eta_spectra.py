import sys
#sys.path.append('/Users/nils/Python_Scripts/Classes/')
#from HistogramClass import Histogram
import numpy as np
import copy
 

class Histogram:
    
    def __init__(self, hist_min, hist_max, num_bins):
        if hist_min > hist_max or hist_min == hist_max:
            raise ValueError('hist_min must be smaller than hist_max')
            
        elif not isinstance(num_bins,int) or num_bins <= 0:
            raise ValueError('Number of bins must be a positive integer')
            
        else:
            self.hist_min = hist_min
            self.hist_max = hist_max
            self.num_bins = num_bins
            self.num_events = 1
            self.histogram = np.zeros(num_bins)
        
        
    def get_histogram(self):
        return self.histogram
    
    
    def get_num_events(self):
        return self.num_events
    
    
    def get_bin_coordinates(self):
        return np.linspace(self.hist_min, self.hist_max, num=self.num_bins)
    
    
    def get_bin_width(self):
        return (self.hist_max - self.hist_min)/(self.num_bins - 1)
    
    
    def add_value(self, value):
        # Case 1.1: value is a single number
        if isinstance(value, (int, float, np.number)):
            
            if value < self.hist_min or value > self.hist_max:
                err_msg = 'Value '+str(value)+' lies outside the histogram '+\
                          'range ['+str(self.hist_min)+','+str(self.hist_max)+\
                          ']. Increase histogram range!'
                raise ValueError(err_msg)
                
            else:
                hist_min = self.hist_min
                hist_max = self.hist_max
                num_bins = self.num_bins
                
                bin_width = (hist_max-hist_min)/(num_bins-1)
                bin_positions = np.linspace(hist_min, hist_max, num=num_bins)
                bin_edges = np.append(bin_positions, bin_positions[-1]+bin_width)-bin_width/2
                
                for i in range(0, num_bins):
                    # Case 2.1: histogram contains only 1 event
                    if self.num_events == 1:
                        if i == 0 and value == bin_edges[0]:
                            self.histogram[0] += 1
                        elif value > bin_edges[i] and value <= bin_edges[i+1]:
                            self.histogram[i] += 1
                    # Case 2.2: If histogram contains multiple events, always add 
                    #           values to the latest event
                    else:
                        if i == 0 and value == bin_edges[0]:
                            self.histogram[-1,0] += 1
                        elif value > bin_edges[i] and value <= bin_edges[i+1]:
                            self.histogram[-1,i] += 1
            
        # Case 1.2: value is a list of numbers
        elif type(value) == list or isinstance(value, np.ndarray):
            for element in value:
                self.add_value(element)
            
        # Case 1.3: value has an invalid input type
        else:
            err_msg = 'Invalid input type! Input value must have one of the '+\
                      'following types: (int, float, np.number, list, np.ndarray)'
            raise TypeError(err_msg)

    
    def add_event(self):
        empty_histogram = np.zeros(self.num_bins)
        self.histogram = np.vstack((self.histogram, empty_histogram))
        
        self.num_events += 1
                
                    
    def get_averaged_histogram(self):
        if self.histogram.ndim == 1:
            raise TypeError('Cannot average an array of dim = 1')
        else:
            average_hist = Histogram(self.hist_min, self.hist_max, self.num_bins)
            average_hist.histogram = np.mean(self.histogram, axis=0)
            
            return average_hist
    
    
    def normalize_histogram_by(self, value):
        self.histogram /= value
        return self
    
        
    def get_std_err(self):
        if self.histogram.ndim == 1:
            raise TypeError('Cannot compute the standard error of an array of dim = 1')
        else:
            return np.std(self.histogram, axis=0)/np.sqrt(self.num_events)
 
    
def load(fname):
    f = open(fname,'r')
    data = []
    for line in f.readlines():
        data.append(line.replace('\n','').split(' '))
    f.close()
    return data


def is_new_event(line):
    if 'event' in line and 'out' in line and line[2] != '0':
        return True
    else:
        return False
    
    
def is_comment(line):
    if '#' in line or line[0].startswith('#!OSCAR'):
        return True
    else:
        return False


def rapidity(line):
    E  = float(line[5])
    pz = float(line[8])
    return np.arctan(pz/E)


def pseudorapidity(line):
    px = float(line[6])
    py = float(line[7])
    pz = float(line[8])
    p  = np.sqrt(px**2 + py**2 + pz**2)
    theta = np.arccos(pz/p)
    return -1.0 * np.log(np.tan(theta/2.0))


def print_averaged_hist_to_file(dictionary, output_path, std_err = False):
    key_list = list(dictionary.keys())
    num_keys_with_err = int(2*len(key_list))
    num_keys_without_err = int(len(key_list))
    first_key = key_list[0]
    
    bin_coordinates = dictionary[first_key].get_bin_coordinates()
    num_bins = (len(bin_coordinates))
    bin_width = dictionary[first_key].get_bin_width()
    
    if std_err == True:
        output_data = np.zeros((num_keys_with_err, num_bins))
    else:
        output_data = np.zeros((num_keys_without_err, num_bins))
    
    counter_line = 0
    for key in key_list:
        bin_width = dictionary[key].get_bin_width()
        data = dictionary[key].get_averaged_histogram().normalize_histogram_by(bin_width).get_histogram()
        
        output_data[counter_line] = data
        counter_line +=1
        
        if std_err == True:
            err = dictionary[key].get_std_err()
            output_data[counter_line] = err
            counter_line +=1
    
    # Get the histogram counts as columns instead of rows
    output_data = np.transpose(output_data)
    
    header = '# bin_centers '
    if std_err == True:
        for key in key_list:
            header += key + ' ' + key + '_error' + ' ' 
    else:
        for key in key_list:
            header += key + ' ' 
      
    output = open(output_path, "w")
    output.write('# event averaged bin counts for given particle species divided by bin width\n')
    output.write(header + '\n')
    for i in range(0,num_bins):
        output.write('{:7.6f}'.format(bin_coordinates[i])+' '+' '.join("{:7.6f}".format(e) for e in output_data[i])+'\n')   
    output.close()
        


############################# Definitions End ################################


print(sys.argv)

FILE_INPUT = sys.argv[4]
DIRECTORY_OUTPUT = sys.argv[5]
#FILE_INPUT = "/Users/nils/smash-vhlle-hybrid/build/Hybrid_Results/RuRu_200.0/1/Sampler/particle_lists.oscar"
FILE_OUTPUT_DNDY = DIRECTORY_OUTPUT + "/dNdy.txt"
FILE_OUTPUT_DNDETA = DIRECTORY_OUTPUT + "/dNdEta.txt"      

hist_min = float(sys.argv[1])
hist_max = float(sys.argv[2])
num_bins = int(sys.argv[3])  
            

dNdy = {
    # Uses PDG code as keys 
    "2212"  : Histogram(hist_min, hist_max, num_bins),  # Proton
    "-2212" : Histogram(hist_min, hist_max, num_bins),  # Anti proton
    "111"   : Histogram(hist_min, hist_max, num_bins),  # Pi0
    "211"   : Histogram(hist_min, hist_max, num_bins),  # Pi+
    "-211"  : Histogram(hist_min, hist_max, num_bins),  # Pi-
    "321"   : Histogram(hist_min, hist_max, num_bins),  # K+
    "-321"  : Histogram(hist_min, hist_max, num_bins),  # K-
    "3122"  : Histogram(hist_min, hist_max, num_bins),  # Lambda
    "-3122" : Histogram(hist_min, hist_max, num_bins),  # Anti lambda
    }
dNdEta = copy.deepcopy(dNdy)

particle_list = load(FILE_INPUT)
pdg_list = list(dNdy.keys())

for line in particle_list:
    
    if is_comment(line) and not is_new_event(line):
        continue
    
    elif is_new_event(line):
        for key in pdg_list:
            dNdy[key].add_event()
            dNdEta[key].add_event()
    
    elif line[9] in pdg_list:
        pdg_code = line[9]
        y = rapidity(line)
        eta = pseudorapidity(line)
        
        dNdy[pdg_code].add_value(y)
        dNdEta[pdg_code].add_value(eta)
    
    else:
        continue

print_averaged_hist_to_file(dNdy, FILE_OUTPUT_DNDY, std_err=True)
print_averaged_hist_to_file(dNdEta, FILE_OUTPUT_DNDETA, std_err=True)

del dNdy
del dNdEta
