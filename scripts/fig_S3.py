"""
Script to visualize significant region eccentricity across task epoch and hand conditions (Figure S3).

This script:
- Loads eccentricity data for significant regions from 'S3_data.xlsx'.
- Plots the distribution of eccentricity values across experimental epochs showing task epoch × hand effects.
- Saves the figure to the FIG_DIR directory.
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
    
def plot_sig_region_eccentricity(ecc, fig_name='S3_task_epoch-hand_effect_sig_regions_ecc.png'):
    """
    Plots the distribution of region eccentricity across experimental epochs for significant regions.

    Parameters
    ----------
    ecc : pd.DataFrame
        DataFrame containing columns ['sub', 'epoch', 'distance'] for region eccentricity analysis.
    fig_name : str, optional
        Output file name for the saved figure.

    """
    epoch_color_map = {
        'leftbaseline': 'orange',
        'rightbaseline': 'green',
        'rightlearning-early': 'green',
        'rightlearning-late': 'green',
        'lefttransfer-early': 'orange',
        'lefttransfer-late': 'orange'
    }
    cmap = list(epoch_color_map.values())
    fig, ax = plt.subplots(figsize=(3, 3))
    data = ecc.groupby(['sub', 'epoch']).mean(numeric_only=True).reset_index()
    epoch_order = list(epoch_color_map.keys())
    data['epoch'] = pd.Categorical(data['epoch'], categories=epoch_order, ordered=True)
    data.sort_values('epoch', inplace=True)
    data.reset_index(drop=True, inplace=True)
    sns.lineplot(data=data, x='epoch', y='distance', errorbar=None, 
                 marker='o', ms=6, lw=1.2, mfc='w', mec='k', color='k', ax=ax)
    sns.stripplot(data=data, x='epoch', y='distance', jitter=.1, 
              zorder=-1, s=5, alpha=.5, palette=cmap, hue='epoch', ax=ax)
    ax.set_xlabel('', fontsize=12, fontweight='bold')

    ticks = [0, 1, 2, 3, 4, 5]
    ax.set_xticks(ticks)
    
    # Set the tick labels with rotation and fontsize
    labels = ['LH Baseline', 'RH Baseline', 'RH Learning Early',
              'RH Learning Late', 'LH Transfer Early', 'LH Transfer Late']
    ax.set_xticklabels(labels, rotation=90, fontsize=14)
    ax.set_yticks(np.arange(1, 4).astype(int))
    ax.set_ylabel('Eccentricity', fontsize=14, fontweight='bold')
    sns.despine()

    fig.savefig(os.path.join(FIG_DIR, fig_name), dpi=300, bbox_inches='tight')

def main():

    data = pd.read_excel(os.path.join(DATA_DIR, 'S3_data.xlsx'))

    plot_sig_region_eccentricity(data)

if __name__ == '__main__':
    main()
