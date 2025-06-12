"""
Script to visualize permutation test boxplots across networks and hemispheres for RH learning and LH transfer eccentricity and the error correlation (Figures S7B and S7E).

This script:
- Loads permutation test and error data from 'S7BE_data.xlsx'.
- Plots boxplots summarizing permutation null distributions for right-hand learning early error and left-hand transfer early error.
- Saves both resulting figures to the FIG_DIR directory.
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure project root is in sys.path for absolute imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.config import FIG_DIR, DATA_DIR
os.makedirs(FIG_DIR, exist_ok=True)

def plot_permute_bplots(data, fig_name, n_perm=1000, p_thresh=0.05):
    """
    Plot permutation null distributions and real correlation values for each hemisphere.

    Parameters
    ----------
    data : pd.DataFrame
        Must include columns ['hemi', 'network', 'r', 'pspin_fdr'] and
        null distribution columns as last `n_perm` columns.
    fig_name : str
        Full name for saving the figure.
    n_perm : int, optional
        Number of permutations (default=1000).
    p_thresh : float, optional
        Significance threshold for coloring real data points (default=0.05).
    """
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    for ax, hemi in zip(axs, ['LH', 'RH']):
        data_hemi = data.query('hemi == @hemi')
        rvals = data_hemi['r'].values
        pspin_fdr = data_hemi['pspin_fdr'].values
        nulls_dist = data_hemi.iloc[:, -n_perm:].T.values

        # Box plots for null distributions
        ax.boxplot(
            nulls_dist,
            patch_artist=True,
            vert=True,
            boxprops={'facecolor': 'lightblue'},
            whis=[0, 100],
            showcaps=True
        )

        # Overlay real correlation values as points
        for i, r in enumerate(rvals):
            color = 'red' if pspin_fdr[i] <= p_thresh else 'blue'
            ax.plot(i + 1, r, color=color, marker='o', markersize=6, zorder=5)

        ax.axhline(0, color='blue', linestyle='dashed', zorder=-1)
        ax.grid(True, axis='x', linestyle='--', alpha=0.5)
        ax.set_xticks(np.arange(1, len(data_hemi['network']) + 1))
        ax.set_xticklabels(
            data_hemi['network'],
            rotation=90,
            ha='center',
            fontsize=12
        )
        ax.tick_params(axis='x', which='both', bottom=False, top=False)
        ax.set(ylim=(-0.45, 0.45))
        sns.despine(ax=ax, bottom=True)
    axs[0].set_ylabel('Spatial Correlation', fontsize=14)
    axs[0].set_title('Left Hemisphere', fontsize=14)
    axs[1].set_title('Right Hemisphere', fontsize=14)
    fig.tight_layout()
    
    fig.savefig(os.path.join(FIG_DIR, fig_name), dpi=300)


def main():

    data = pd.read_excel(os.path.join(DATA_DIR, 'S7BE_data.xlsx'), sheet_name=None)
    
    fig_name =  'S7B_RH_Learning_permutaions.png'
    plot_permute_bplots(data['rightlearning-early_error_spins'], fig_name)

    fig_name = 'S7E_LH_transfer_permutaions.png'
    plot_permute_bplots(data['lefttransfer-early_error_spins'], fig_name)

if __name__ == '__main__':
    main()
