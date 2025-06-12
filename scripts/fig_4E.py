"""
Script to visualize the hand effect on statistical maps and significant region eccentricity (Figure 4E).

This script:
- Loads hand effect statistical and eccentricity data from '4E_data.xlsx'.
- Plots pairwise statistical maps comparing right and left hand effects.
- Plots the distribution of eccentricity for significant regions across hemispheres and epochs.
- Saves all output figures to the FIG_DIR directory.
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

from utils import plotting
from utils.config import FIG_DIR, DATA_DIR
os.makedirs(FIG_DIR, exist_ok=True)
    
def plot_hand_effect(data, prefix='4E_'):
    """
    Plot pairwise statistical maps for hand effect analysis.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the relevant statistics for hand effect maps.
    prefix : str, optional
        Prefix for the output file name.
    """
    vmax = 6.11
    vmin = 2.26
    os.makedirs(FIG_DIR, exist_ok=True)
    plotting.pairwise_stat_maps(
        data,
        os.path.join(FIG_DIR, prefix),
        vmax=vmax,
        vmin=vmin
    )

def plot_sig_region_eccentricity(ecc, fig_name='4E_hand_effect_sig-regions_ecc.png'):
    """
    Plot region eccentricity for significant hand effect regions.

    Parameters
    ----------
    ecc : pd.DataFrame
        DataFrame with columns ['hemi', 'sub', 'epoch', 'distance'].
    fig_name : str
        Name of the figure file to save.
    """
    # Epoch ordering and color palette
    epoch_color_map = {
        'leftbaseline': 'orange',
        'rightbaseline': 'green',
        'rightlearning-early': 'green',
        'rightlearning-late': 'green',
        'lefttransfer-early': 'orange',
        'lefttransfer-late': 'orange'
    }
    cmap = list(epoch_color_map.values())
    fig, axs = plt.subplots(1, 2, figsize=(6, 3.5))
    
    for ax, hemi in zip(axs, ['LH', 'RH']):
        data = ecc.query('hemi == @hemi').copy()
        data = data.groupby(['sub', 'epoch']).mean(numeric_only=True).reset_index()
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
        sns.despine()

    axs[0].set_ylabel('Eccentricity', fontsize=14, fontweight='bold')
    axs[1].set_ylabel('')
    axs[0].set_title('Left Hemisphere', fontsize=14)
    axs[1].set_title('Right Hemisphere', fontsize=14)

    fig.savefig(os.path.join(FIG_DIR, fig_name), dpi=300)

def main():

    data = pd.read_excel(os.path.join(DATA_DIR, '4E_data.xlsx'), sheet_name=None)

    plot_hand_effect(data['hand_effect_right_vs_left'])

    plot_sig_region_eccentricity(data['right_vs_left_eccentricity'])


if __name__ == '__main__':
    main()
