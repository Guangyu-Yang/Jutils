# Jutils
Jutils alpha version

Jutils is a visuliation tools kits for showing alternative splicing events. It support vizualizing results generated from AS event detectors: MntJULiP, LeafCutter, MAJIQ and rMATs.

Jutils contains 4 components,
(1) Convert program results to a unified tab saperated file (TSV)
(2) Receive input of the TSV file (from (1)) and plot the heatmaps
(3) Receive input of the TSV file or bam files, and plot the sashimi plot for the given region that are interested
(4) Receive input of the TSV files and plot the Venn Diagram with predicted AS genes.

## Usage by examples
```
## test pairwise comparison
# generate TSV file from MntJULiP output
result_dir='path/to/MntJULiP_results_dir'
python3 jutils.py convert-results --mntjulip-dir ${result_dir}

# heatmap: DSR events with aggregate by groups/clusters
python3 jutils.py heatmap --tsv-file 'mntjulip_DSR_results.tsv' \
                          --meta-file 'meta_file.tsv' \
                          --dpsi 0.3 --p-value 0.05 --q-value 0.05 --aggregate

# heatmap: DSR events without aggregate
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


# heatmap: DSR without aggregate
python3 jutils.py heatmap --tsv-file 'mntjulip_DSR_results.tsv' \
                          --meta-file 'meta_file_4.tsv' \
                          --dpsi 0.3 --p-value 0.05 --q-value 0.05

# heatmap: DSA
python3 jutils.py heatmap --tsv-file 'mntjulip_DSA_results.tsv' \
                          --meta-file 'meta_file_4.tsv' \
                          --p-value 0.05 --q-value 0.05 --avg 200
```
