"""
Script to visualize mean BOLD signal for significant regions by hand and task epoch (Figure S4).

This script:
- Loads mean BOLD data for significant regions from 'S4_data.xlsx'.
- Plots the group-average BOLD z-score for main effects of hand and of task epoch.
- Saves the resulting figure to the FIG_DIR directory.
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

def plot_sig_region_bold(data, ax):
    """
    Plot group BOLD Z-score for significant regions across epochs.
    
    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with columns ['epoch', 'tmean'].
    ax : matplotlib.axes.Axes
        Axes object to plot on.
    
    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes containing the plot.
    """
    epoch_color_map = {
        'leftbaseline': 'orange',
        'rightbaseline': 'green',
        'rightlearning-early': 'green',
        'rightlearning-late': 'green',
        'lefttransfer-early': 'orange',
        'lefttransfer-late': 'orange'
    }
    labels = ['LH Baseline', 'RH Baseline', 'RH Learning Early',
              'RH Learning Late', 'LH Transfer Early', 'LH Transfer Late']
    cmap = list(epoch_color_map.values())
    sns.lineplot(data=data, x='epoch', y='tmean', errorbar=None, 
                 marker='o', ms=6, lw=1.2, mfc='w', mec='k', color='k', ax=ax)
    sns.stripplot(data=data, x='epoch', y='tmean', jitter=.1, 
              zorder=-1, s=5, alpha=.5, palette=cmap, hue='epoch', ax=ax)
    ax.set_xlabel('', fontsize=12, fontweight='bold')
    ax.set_ylabel('z-score', fontsize=12)
    ax.set_xticks(range(len(epoch_color_map)))
    ax.set_xticklabels(labels, rotation=90, fontsize=12)
    ax.set_yticks(np.arange(-.4, .5, .2))
    sns.despine()
    return ax
    
def main():

    data = pd.read_excel(os.path.join(DATA_DIR, 'S4_data.xlsx'), sheet_name=None)
    
    fig, axs = plt.subplots(1, 2, figsize=(6, 3))
    plot_sig_region_bold(data['hand_sig_regions_bold'], ax=axs[0])
    plot_sig_region_bold(data['task_epoch_sig_regions_bold'], ax=axs[1])
    axs[0].set_title('Main Effect of Hand', fontsize=14)
    axs[1].set_title('Main Effect of Task Epoch', fontsize=14)
    plt.subplots_adjust(wspace=0.5)

    fig.savefig(os.path.join(FIG_DIR, 'S4_average_bold_across_significant_regions.png'), dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    main()