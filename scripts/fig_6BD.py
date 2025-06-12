"""
Script to visualize re-expression of region eccentricity for task epoch and hand comparisons (Figure 6BD).

This script:
- Loads region eccentricity and posthoc statistical data from '6BD_data.xlsx'.
- Plots re-expression of region eccentricity for significant regions across task epochs and across hands
- Marks statistical significance between epochs/hands using posthoc test results.
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

def plot_reexpression(ecc_data, posthoc, ax=None):
    """
    Plot re-expression of region eccentricity across selected epochs, with posthoc significance.

    Parameters
    ----------
    ecc_data : pd.DataFrame
        DataFrame with columns ['epoch', 'distance'] and (optionally) 'subject'.
    posthoc : pd.DataFrame
        DataFrame with columns ['A', 'B', 'p-unc'] for pairwise comparisons.
    ax : matplotlib.axes.Axes, optional
        Axes object to plot on.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes containing the plot.
    """
    epoch_order = ["rightlearning-late", "lefttransfer-early", "lefttransfer-late"]
    display_names = ["RH Learning Late", "LH Transfer Early", "LH Transfer Late"]

    # Set categorical order
    ecc_data = ecc_data.copy()
    ecc_data['epoch'] = pd.Categorical(ecc_data['epoch'], categories=epoch_order, ordered=True)

    # Main plots
    sns.lineplot(
        data=ecc_data, x='epoch', y='distance', errorbar=None,
        marker='o', ms=8, lw=1.5, mfc='w', mec='k', color='k', ax=ax
    )
    sns.stripplot(
        data=ecc_data, x='epoch', y='distance',
        ax=ax, size=8, hue='epoch', legend=False,
        jitter=.05, zorder=-1
    )

    # Mark significance
    if posthoc is not None and not posthoc.empty:
        sig_results = posthoc[posthoc['p-unc'] < 0.05]
        epoch_to_x = {epoch: i for i, epoch in enumerate(epoch_order)}
        y_max = ecc_data['distance'].max()
        y_offset = 0.1 * (ecc_data['distance'].max() - ecc_data['distance'].min() + 1e-6)
        for i, (epoch_a, epoch_b, p_value) in enumerate(sig_results[['A', 'B', 'p-unc']].values):
            x1, x2 = epoch_to_x[epoch_a], epoch_to_x[epoch_b]
            y_pos = y_max + (i + 1) * y_offset
            sig_label = '*' if p_value < 0.05 else ''
            ax.plot([x1, x2], [y_pos, y_pos], color='black', linewidth=1.5)
            ax.text((x1 + x2) / 2, y_pos - 0.03, sig_label, ha='center', va='bottom',
                    fontsize=22, color='black')

    # Axis formatting
    ax.set_xlabel('')
    ax.set_ylabel('Correlation (r)', fontsize=14)
    ax.set_xticks(range(len(epoch_order)))
    ax.set_xticklabels(display_names, rotation=90, fontsize=14)
    sns.despine(ax=ax)

    return ax

def main():

    data = pd.read_excel(os.path.join(DATA_DIR, '6BD_data.xlsx'), sheet_name=None)
    
    fig, axs = plt.subplots(1, 2, figsize=(4.5, 6))
    
    ecc_data = data['epoch_sig_regions_eccentricity']
    posthoc = data['epoch_re_expression']
    plot_reexpression(ecc_data, posthoc, ax=axs[0])
    
    ecc_data = data['hand_sig_regions_eccentricity']
    posthoc = data['hand_re_expression']
    plot_reexpression(ecc_data, posthoc, ax=axs[1])

    axs[0].set_title('Task Epoch', fontsize=14)
    axs[1].set_title('Hand', fontsize=14)
    plt.tight_layout()
    
    fig.savefig(os.path.join(FIG_DIR, '6BD_task_epoch_hand_reexpression.png'), dpi=300)
    
if __name__ == '__main__':
    main()