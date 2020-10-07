import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def plot_heatmap(file, meta_file, out_dir, p_value_threhold, q_value_threhold, dpsi_threshold, foldchange_threshold, avg_threshold, aggregate):
    def process_group(x):
        start, end = float('inf'), 0
        for label in x['FeatureLabel']:
            _chr, coord = label.split(':')
            _start, _end = (int(v) for v in coord.split('-'))
            start, end = min(start, _start), max(end, _end)
        return f"{x['GeneName'].iloc[0]}_{_chr}:{start}-{end}"

    samples = []
    conditions = []
    with open(meta_file, 'r') as f:
        for line in f:
            sample, cond = line.strip().split('\t')
            samples.append(sample)
            conditions.append(cond)

    data_df = pd.read_csv(file, sep='\t', comment='#')
    data_df = data_df[data_df['p-value'] < p_value_threhold]
    data_df = data_df[data_df['q-value'] < q_value_threhold]
    data_df = data_df[data_df['GeneName'] != '.']
    original_columns = data_df.columns

    if 'dPSI' in original_columns:
        if data_df.shape[1] > 14 and aggregate:
            print("Multi-way comparison doesn't support aggregate mode, change to non-aggregate mode instead")
            aggregate = False

        if aggregate:
            selected_groups = data_df[abs(data_df['dPSI']) > dpsi_threshold]['GroupID'].drop_duplicates()
            data_df = data_df[data_df['GroupID'].isin(selected_groups)]
            data_df = data_df[data_df['dPSI'] > 0]
            new_data_df = data_df['PSI'].str.split(',', expand=True).astype(float)
            new_data_df.columns = samples
            new_data_df[['GeneName', 'FeatureLabel', 'GroupID']] = data_df[['GeneName', 'FeatureLabel', 'GroupID']]
            groups = new_data_df.groupby(['GroupID'])
            data_df = groups.apply(lambda x: np.sum(x[samples], axis=0))
            data_df.index = groups.apply(process_group)
        else:
            data_df = data_df[abs(data_df['dPSI']) > dpsi_threshold]
            new_data_df = data_df['PSI'].str.split(',', expand=True).astype(float)
            new_data_df.columns = samples
            new_data_df['index'] = data_df[['GeneName', 'FeatureLabel']].agg('_'.join, axis=1)
            new_data_df['dPSI'] = data_df['dPSI']
            groups = new_data_df.groupby(['index'])
            data_df = groups.apply(lambda x: x.iloc[x['dPSI'].argmax()])
            data_df = data_df.drop(columns=['dPSI', 'index'])
    elif 'log2FoldChange' in original_columns:
        data_df = data_df[foldchange_threshold < abs(data_df['log2FoldChange'])]
        data_df = data_df[abs(data_df['log2FoldChange']) < float('inf')]
        data_df = data_df[data_df.iloc[:, 12:].apply(lambda x: np.any(x > avg_threshold) ,axis=1)]
        new_data_df = data_df['ReadCount1'].str.split(',', expand=True).astype(float)
        new_data_df.columns = samples
        new_data_df.index = data_df[['GeneName', 'FeatureLabel']].agg('_'.join, axis=1)
        data_df = new_data_df

    num, max_num = data_df.shape[0], 500
    if num > max_num:
        data_df = data_df.iloc[:max_num, :]
        print(f'Warming: the number of selected events ({num}) are > {max_num}, will only should the first {max_num} events in the heatmaps')
    mask = data_df.isnull()
    data_df = data_df.fillna(0)

    clustermapParams = {
        'square':False # Tried to set this to True before. Don't: the dendograms do not scale well with it.
    }
    figureWidth = data_df.shape[1] / 4
    figureHeight= data_df.shape[0] / 4
    if figureHeight < 15:
        figureHeight = 15
    if figureWidth < 15:
        figureWidth = 15

    method = 'average'
    metric = 'braycurtis'

    figure = sns.clustermap(data_df, cmap="RdBu_r", col_cluster=False, z_score=0, vmin=-5, vmax=5,
                            metric=metric, method=method, mask=mask,
                            yticklabels=1, xticklabels=1, figsize=(figureWidth, figureHeight), **clustermapParams)

    figure.ax_heatmap.set_facecolor("lightyellow")
    figure.savefig(out_dir / 'clustermap_Z.png')
    plt.close()

    figure = sns.clustermap(data_df, cmap="RdBu_r", z_score=0, vmin=-5, vmax=5,
                            metric=metric, method=method, mask=mask,
                            yticklabels=1, xticklabels=1, figsize=(figureWidth, figureHeight), **clustermapParams)

    figure.ax_heatmap.set_facecolor("lightyellow")
    figure.savefig(out_dir / 'clustermap2_Z.png')
    plt.close()

    if 'dPSI' in original_columns:
        figure = sns.clustermap(data_df, cmap=sns.cm.rocket_r, col_cluster=False,
                                metric=metric, method=method, mask=mask,
                                yticklabels=1, xticklabels=1, figsize=(figureWidth, figureHeight), **clustermapParams)

        figure.ax_heatmap.set_facecolor("lightyellow")
        figure.savefig(out_dir / 'clustermap.png')
        plt.close()

        figure = sns.clustermap(data_df, cmap=sns.cm.rocket_r,
                                metric=metric, method=method, mask=mask,
                                yticklabels=1, xticklabels=1, figsize=(figureWidth, figureHeight), **clustermapParams)

        figure.ax_heatmap.set_facecolor("lightyellow")
        figure.savefig(out_dir / 'clustermap2.png')
        plt.close()
