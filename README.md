# Jutils

Jutils (alpha_1.0) is a visualization toolkit for alternative splicing events. Jutils supports vizualizing results generated by the differential splicing (DS) detection tools MntJULiP, LeafCutter, MAJIQ and rMATS, and can be easily adapted to use with other DS software.

Described in:

      Yang G, Cope L, He Z, and Florea L. Jutils: A visualization toolkit for differential alternative splicing events, *Submitted*.

```
Copyright (C) 2020-2021, and GNU GPL v3.0, by Guangyu Yang, Liliana Florea
```

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.  

### <a name="table-of-contents"></a> Table of contents
- [What is Jutils?](#what-is-jutils)
- [Installation](#installation)
- [Usage](#usage)
- [Input/Output](#inputoutput)
- [Support](#support)

### <a name="what-is-jutils"></a> What is Jutils?
Jutils is a visualization toolkit for alternative splicing events. It uses an intermediate tab separated file (TSV) to represent alternative splicing data such as that generated by a differential splicing prediction program. Jutils supports the vizualization of results generated by popular differential splicing (DS) prediction tools MntJULiP, LeafCutter, MAJIQ and rMATs. Additionally, users can write their own routines to convert the output of any other DS program into the unified TSV data format, which can then be visualized with Jutils.

Jutils provides three types of visualization: *heatmaps*, *sashimi plots*, and *Venn diagrams*. The user can display all records in the file, or can apply filters to select specific subsets of the data, for instance statistically significant differentially spliced features.

### <a name="installation"></a> Installation
MntJULiP is written in Python. To download the source code, clone this GitHub repository:

```
git clone https://github.com/Guangyu-Yang/Jutils.git
```

#### System requirements
* Linux or Darwin  
* Python 3.7 or later

#### Prerequisites
Required Python packages: pandas, numpy, seaborn, matplotlib. The Python packages can be installed with the command:   
```
pip install --user pandas numpy seaborn matplotlib
```

### <a name="usage"></a>  Usage
Jutils works in two steps. *Step 1* generates the TSV file representation of the user data. *Step 2* uses the TSV file, along with other information optionally provided by the user, to generate visualizations. The basic commands are listed here, and examples as applied to the specific visualizations are given below.


#### Basic usage

##### TSV file conversion
```
python3 jutils.py convert-results [ --mntjulip-dir | --leafcutter-dir | --majiq-dir | rmats-dir ] <dsprogram_result_dir>
```
The command takes as input the directory containing the output from the specified DS tool, and generates a TSV file in the current(?) directory. 

##### Heatmap visualization
```
python3 jutils.py heatmap --tsv-file <tsv_file> --meta-file <meta_file> [options]
        options:
        --dpsi        cutoff for delta PSI (Percent Splice In)
        --p-value     cutoff for differential test p-value
        --q-value     cutoff for differential test q-value
        --aggregate   show results at group level (select one intron per group)
```
The meta file lists the condition for each sample for representation on the heatmap, for instance when the data has been generated from a differential analysis. The p-value, q-value and dPSI values are those generated by the DS tool and stored in the TSV file. The format of the TSV file is shown here, and that of the metadata file is here. Some programs including LeafCutter and MntJULiP represent introns as part of a group, and may report multiple DS introns per group. The --aggregate option selects one representative intron per group to include in the display. The selection procedure is described here.  

##### Sashimi visualization
```
python3 jutils.py sashimi --tsv-file <tsv_file> --meta-file <meta_file> [ --group-id <group_id> | --coordinate <coords> ] [options]
        where:
        --group_id     select group to visualize
        --coordinate   select genomic range for visualization
        options:
        --gtf          GTF file of gene annotations to add to the display
```
The streamlined command above will use solely information contained in the TSV and metadata files for visualization. Introns will be displayed with the values (e.g., read counts, PSI value) in multiple samples, separately by the conditions specified in the metadata file. Flanking introns will be shown at a fixed coverage level (15(?)). Alternatively, the command below extracts the information on flanking exon coverage from the BAM files and generates traditional sashimi visualizations:

```
python3 jutils.py sashimi --bam-list <bam_list.tsv> [ --group-id <group_id> | --coordinate <coords> ] [options]
        where:
        --group_id     select group to visualize
        --coordinate   select genomic range for visualization
        options:
        --gtf          GTF file with gene annotations to add to the display
```
The format of the BAM list file is here.

##### Venn diagram visualization
```
Insert command usage here
```
The command above creates Venn diagram representations of gene sets from multiple TSV files, corresponding to multiple tools or comparisons.

#### Usage customized by program

##### LeafCutter
LeafCutter represents alternative splicing events at the intron level, with introns having common endpoints further organized into a group. LeafCutter uses a differential splicing ratio test on an intron within its group to identify DS events. The Percent Splice In (PSI) value of each intron in a group as calculated from the raw read counts is then used by Jutils to generate heatmaps. The visualization program generates both raw and Z-score normalized heatmaps. LeafCutter may report more than one DS intron per group; the --aggregate option can be used to select a representative intron (?).

The following is an example of a script for processing and visualizing results from LeafCutter using heatmaps:

```
# convert LeafCutter output to TSV format
result_dir='path/to/LeafCutter_results_dir'
python3 jutils.py convert-results --leafcutter-dir ${result_dir}

# heatmap: visualize DSR events
python3 jutils.py heatmap --tsv-file 'leafcutter_DSR_results.tsv' \
                          --meta-file 'meta_file.tsv' \
                          --dpsi 0.2 --p-value 0.05 --q-value 0.05                       
```

##### MntJULiP
MntJULiP detects differentially spliced introns using two types of tests. The first is a differential splicing ratio (DSR) test of an intron within its group, similar in function to LeafCutter. The second is a differential test on the (normalized) abundance level of the intron (DSA). We first describe the use of Jutils for MntJULiP(DSR), and then describe semantic and data changes corresponding to the MntJULiP(DSA) test below.

The MntJULiP(DSR) test evaluates each intron within its group ('bunch'). Groups contain all introns sharing the same splice junction. PSI values for representation into heatmaps are calculated from the raw read counts in each sample. MntJULiP may report more than one DS intron per group; the --aggregate option can be used to select a representative value per group, as described here.

The MntJULiP(DSA) test evaluates each intron independently. Instead of PSI values, the program reports (and the TSV file contains) the normalized read counts averaged for each condition, from which the fold change can be calculated. The heatmaps represent abundance values calculated from the read counts in each sample. The 'semantically' modified TSV file is described below.

Additionally, MntJULiP can perform both traditional pairwise comparisons, such as 'cases' versus 'controls', as well as comparisons of multiple conditions, a feature that is unique to MntJULiP.  

Examples of scripts for all of these options are provided below:

```
###### pairwise comparison

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


###### multi-way comparison
# generate TSV file from MntJULiP output
result_dir='path/to/MntJULiP_results_dir'
python3 jutils.py convert-results --mntjulip-dir ${result_dir}

# heatmap: DSR without aggregation
python3 jutils.py heatmap --tsv-file 'mntjulip_DSR_results.tsv' \
                          --meta-file 'meta_file_multi.tsv' \
                          --dpsi 0.3 --p-value 0.05 --q-value 0.05

# heatmap: DSA
python3 jutils.py heatmap --tsv-file 'mntjulip_DSA_results.tsv' \
                          --meta-file 'meta_file_multi.tsv' \
                          --p-value 0.05 --q-value 0.05 --avg 200
```

Sashimi visualizations use the raw read counts per sample, as before:
```
####### sashimi plot : 
python3 jutils.py convert-results --mntjulip-dir ${result_dir}

# sashimi plot with bams
python3 jutils.py sashimi --bam-list 'bam_list.tsv' \
                          --coordinate 'chr19:35744400-35745150'

# sashimi plot without bams
python3 jutils.py sashimi --meta-file 'meta_file.tsv' \
                          --tsv-file 'mntjulip_DSR_results.tsv' \
                          --group-id 'g001499' \
                          --gtf 'gencode.v27.transcripts.gtf'
```

##### rMATS
Unlike LeafCutter, MntJULiP and MAJIQ, which are intron-oriented, rMATS reports differential splicing of canonical alternative splicing events (ASEs), including exon skipping, mutually exclusive exons, alternative 5' and 3' splice site and intron retention. (NOTE: Only XXXXX events can be represented with Jutils.) The heatmaps represent PSI values of the ASEs, as reported by rMATS. As with the other programs, intron supporting read counts are shown on the sashimi plots.

```
# convert rMATS output to TSV format
result_dir='path/to/rMATS_results_dir'
python3 jutils.py convert-results --rmats-dir ${result_dir}

# heatmap: visualize DSR events
python3 jutils.py heatmap --tsv-file 'rmats_DSR_results.tsv' \
                          --meta-file 'meta_file.tsv' \
                          --p-value 0.05 --q-value 0.05                       
```
##### Gene set comparison
Jutils provides visualizations of gene sets, as generated by different comparisons and/or methods and represented in TSV files, as a Venn diagram showing their overlap.

```
####### Venn diagram
python3 jutils.py convert-results --leafcutter-dir '/path/to/LeafCutter_results/' \
                                  --mntjulip-dir '~/path/to/MntJULiP_results/' \
                                  --rmat-dir '~/path/to/rMATS_results/'

python3 jutils.py venn-diagram --tsv-file-list tsv_file_list.txt
```
***ADD: what is the tsv-file-list? what does it look like?***

### <a name="inputoutput"></a> Input/Output

#### The unified TSV file
The TSV file contains 14 columns, describing the following attributes (for a DSR test):

```
**Show the header and 2 lines from a DSR file
```

The following slightly modified format, which changes the meaning of several columns, is used for DSA types of comparisons:
```
new header and explanation of columns
```

#### The meta-file
The meta-file is a TAB ('\t') separated file that lists the sample name and condition, for example:
```
sample1  ctrl
sample2  ctrl
sample3  case
sample4  case
```
#### The bam_list file
The bam list file lists the full paths to the BAM alignments files used by the (traditional) sashimi visualization:
```
/path/to/BAM_1
/path/to/BAM_2
...
```
***NOTE: how about the labels/ aliases for visualizations?***

#### The tsv_file_list
The TSV file list for Venn diagram visualizations contains the full path (***AND ALIASES?***) of the TSV files generated for the various comparisons.
```
/path/to/TSV_for_method_1
/path/to/TSV_for_method_2
/path/to/TSV_for_method_3
```

### <a name="support"></a> Support
Contact: gyang22@jhu.edu

### License information
See the file LICENSE for information on the history of this software, terms
& conditions for usage, and a DISCLAIMER OF ALL WARRANTIES.
