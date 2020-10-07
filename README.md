# Jutils
Jutils alpha version

## Usage:
```
####### test pairwise comparison
result_dir='path/to/MntJULiP_results_dir'
python3 jutils.py convert-results --mntjulip-dir ${result_dir}

# DSR with aggregate
python3 jutils.py heatmap --tsv-file 'mntjulip_DSR_results.tsv' \
                          --meta-file 'meta_file.tsv' \
                          --dpsi 0.3 --p-value 0.05 --q-value 0.05 --aggregate

# DSR without aggregate
python3 jutils.py heatmap --tsv-file 'mntjulip_DSR_results.tsv' \
                          --meta-file 'meta_file.tsv' \
                          --dpsi 0.3 --p-value 0.05 --q-value 0.05

# DSA
python3 jutils.py heatmap --tsv-file 'mntjulip_DSA_results.tsv' \
                          --meta-file 'meta_file.tsv' \
                          --p-value 0.05 --q-value 0.05 --avg 200 --fold-change 3



####### test multi-way comparison
result_dir='path/to/MntJULiP_results_dir'
python3 jutils.py convert-results --mntjulip-dir ${result_dir}


# DSR without aggregate
python3 jutils.py heatmap --tsv-file 'mntjulip_DSR_results.tsv' \
                          --meta-file 'meta_file_4.tsv' \
                          --dpsi 0.3 --p-value 0.05 --q-value 0.05

# DSA
python3 jutils.py heatmap --tsv-file 'mntjulip_DSA_results.tsv' \
                          --meta-file 'meta_file_4.tsv' \
                          --p-value 0.05 --q-value 0.05 --avg 200
```
