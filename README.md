# Jutils
Jutils alpha version

Jutils is a visualization tools kits for showing alternative splicing events. It support vizualizing results generated from AS event detectors: MntJULiP, LeafCutter, MAJIQ and rMATs.

Copyright (C) 2020-2021, and GNU GPL v3.0, by Guangyu Yang, Liliana Florea

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.  

### <a name="table-of-contents"></a> Table of contents
- [What is Jutils?](#what-is-jutils)
- [Installation](#installation)
- [Usage](#usage)
- [Input/Output](#inputoutput)
- [Support](#support)

### <a name="what-is-jutils"></a> What is Jutils?
Jutils is a visualization tools kits for showing alternative splicing events. It support vizualizing results generated from AS event detectors: MntJULiP, LeafCutter, MAJIQ and rMATs.

Jutils contains 4 components    
(1) Convert program results to a unified tab saperated file (TSV)    
(2) Receive input of the TSV file (from (1)) and plot the heatmaps    
(3) Receive input of the TSV file or bam files, and plot the sashimi plot for the given region that are interested    
(4) Receive input of the TSV files and plot the Venn Diagram with predicted AS genes.

### <a name="installation"></a> Installation
MntJULiP is written in Python. To download the source code, clone this GitHub repository:

```
git clone https://github.com/Guangyu-Yang/Jutils.git
```

#### System requirements
* Linux or Mac  
* Python 3.7 or later

#### Prerequisites
Required Python packages: pandas, numpy, seaborn, matplotlib, The Python packages can be installed by command   
```
pip install --user pandas numpy seaborn matplotlib
```

### <a name="usage"></a>  Usage by examples
```
## test pairwise comparison
# generate TSV file from MntJULiP output
result_dir='path/to/MntJULiP_results_dir'
python3 jutils.py convert-results --mntjulip-dir ${result_dir}

# heatmap: DSR events aggregated by groups/clusters
python3 jutils.py heatmap --tsv-file 'mntjulip_DSR_results.tsv' \
                          --meta-file 'meta_file.tsv' \
                          --dpsi 0.3 --p-value 0.05 --q-value 0.05 --aggregate

# heatmap: DSR events without aggregation
python3 jutils.py heatmap --tsv-file 'mntjulip_DSR_results.tsv' \
                          --meta-file 'meta_file.tsv' \
                          --dpsi 0.3 --p-value 0.05 --q-value 0.05

# heatmap: DSA events
python3 jutils.py heatmap --tsv-file 'mntjulip_DSA_results.tsv' \
                          --meta-file 'meta_file.tsv' \
                          --p-value 0.05 --q-value 0.05 --avg 200 --fold-change 3



####### test multi-way comparison
result_dir='path/to/MntJULiP_results_dir'
python3 jutils.py convert-results --mntjulip-dir ${result_dir}


# heatmap: DSR without aggregation
python3 jutils.py heatmap --tsv-file 'mntjulip_DSR_results.tsv' \
                          --meta-file 'meta_file_4.tsv' \
                          --dpsi 0.3 --p-value 0.05 --q-value 0.05

# heatmap: DSA
python3 jutils.py heatmap --tsv-file 'mntjulip_DSA_results.tsv' \
                          --meta-file 'meta_file_4.tsv' \
                          --p-value 0.05 --q-value 0.05 --avg 200
```

### <a name="inputoutput"></a> Input/Output
#### Input files
meta-file: a TAB ('\t') seperated file that contains sample name and condition, e.g.
```
s1  ctrl
s2  ctrl
s3  case
s4  case
```

### <a name="support"></a> Support
Contact: gyang22@jhu.edu

#### License information
See the file LICENSE for information on the history of this software, terms
& conditions for usage, and a DISCLAIMER OF ALL WARRANTIES.
