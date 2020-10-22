"""
This script is the .py version of the data I/O section of the notebook "TabulaMuris_Tutorial.ipynb". 
The notebook can be found here:
        https://github.com/SindiLab/SingleCell-Tutorial-Python/blob/main/TabulaMuris/Notebook/TabulaMuris_Tutorial.ipynb

Before running this script, make sure you have the following:

1. Data:
1.1 You can Download the data using 
	wget https://github.com/chanzuckerberg/scRNA-python-workshop/raw/master/content/data.zip

1.2 Unzip
	unzip data.zip
	
1.3 Rename the folder to be called "TMData".

2. Libraries 
all required libraries are listed in "requirements.txt" and can be install through
	pip install -r requirements.txt
	
or you can manually download the following:

2.1. Pandas
	pip install pandas

2.2 Scanpy
	pip install scanpy


for more description of the code, refer to the associated notebook 

"""

import pandas as pd
import scanpy as sc

# get in the brain count
brain_count = pd.read_csv("./TM_Data/brain_counts.csv", sep = ',', header = "infer", index_col = 0, error_bad_lines = True)

# output the number of samples and genes 
print(f"Number of Unique Cells: {len(brain_count)}")
print(f"Number of Genes: {len(brain_count.columns)}")

# read in meta data
brain_meta = pd.read_csv("./TM_Data/brain_metadata.csv", sep = ',', header = "infer", index_col = 0, error_bad_lines = True)

# output some stats (used here for example)
print(pd.value_counts(brain_meta['subtissue']))
print("----------")
print(pd.value_counts(brain_meta['mouse.sex']))

# create a scapy object to store the data in the annotated format 
annotated_data = sc.AnnData(X = brain_count, obs =brain_meta)

# since this data is from smartseq, we should try to see how many spike ins we may have 
## and annotate them properly 

spike_dict = dict();
spike_counter = 0;

for genes in annotated_data.var_names:
    if 'ERCC' in genes:
        spike_dict[genes] = True;
        spike_counter+=1;
    else:
        spike_dict[genes] = False;        
        
print(f"Found {spike_counter} many Spike-Ins in the data")

annotated_data.var['ERCC'] = pd.Series(spike_dict);

#and now we want to save the data in the AnnData format
annotated_data.write('./brain_AnnData.h5ad')

# Fin
