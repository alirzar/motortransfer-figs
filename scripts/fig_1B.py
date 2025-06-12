"""
Script to visualize behavioral learning curves and early error changes across task conditions (Figure 1B).

This script:
- Loads subject-level and group-level behavioral data from '1B_data.xlsx'.
- Plots the binned group-average angular error across trials and task blocks.
- Plots the change in early error between RH learning and LH transfer epochs.
- Saves figures to the FIG_DIR directory.
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker, gridspec
import seaborn as sns
import pingouin as pg

# Ensure project root is in sys.path for absolute imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.config import FIG_DIR, DATA_DIR
os.makedirs(FIG_DIR, exist_ok=True)

def plot_task_behaviour_binned(data, trial_block_length = 8,
                               fig_name = '1B_task_plot_binned.png'):
    """
    Plot binned group-average error across the task, by block.

    Parameters
    ----------
    data : pd.DataFrame
        Subject-level, trial-wise data.
    trial_block_length : int, optional
        Length of each trial block. Default is 8.
    fig_name : str, optional
        Output file name for the figure.
    """
    epochs = {1: 'LH Baseline', 2: 'RH Baseline', 3: 'RH Learning', 5: 'Report', 6: 'LH Learning'}
    # Plot setup
    unique_blocks = sorted(data['BlockNo'].unique())
    ncols = len(unique_blocks)
    first_subject = data['SubNo'].unique()[0]
    
    width_ratios = [
        len(data[(data['BlockNo'] == b) & (data['SubNo'] == first_subject)]) / 64
        for b in unique_blocks
    ]

    
    fig = plt.figure(figsize=(16, 4))
    spec = gridspec.GridSpec(
        ncols=ncols, nrows=1, width_ratios=width_ratios,
        wspace=0.03, hspace=0.5, height_ratios=[1]
    )
    
    for i, block in enumerate(unique_blocks):
        block_data = data.query('BlockNo == @block')
        trial_blocks = block_data['TrialBlock'].unique()
        color = 'orange' if np.isin([1, 6], block).any() else 'green'
        
        ax = fig.add_subplot(spec[i])
        sns.lineplot(
            x='TrialBlock', y='AngularError', data=block_data,
            errorbar=('ci', 95), color=color, ax=ax, zorder=3
        )
        
        plt.setp(ax.collections[0], alpha=0.25)
        ax.set(
            xticks=[trial_blocks.max()],
            yticks=np.arange(-15, 60, 15)
        )
        # Optional: shade a particular block (e.g., n == 5)
        if block == 5:
            ax.axvspan(trial_blocks.min(), trial_blocks.max(), color='gray', alpha=0.2)
        
        # Axis formatting
        if i > 0:
            ax.yaxis.set_visible(False)
            sns.despine(ax=ax, left=True)
        else:
            ax.set_ylabel('Angular error (°)', fontsize=12, fontweight='bold')
            sns.despine(ax=ax, left=False)
        ax.set_xlabel('Trial Block', fontsize=12, fontweight='bold') if block == 3 else ax.set_xlabel('')
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(2))
        ax.xaxis.tick_bottom()
        ax.axhline(0, lw=1, c='k', ls='--')
        ax.set_title(epochs[block])

    fig.savefig(os.path.join(FIG_DIR, fig_name), dpi=300)

def plot_early_error_change(early_error, fig_name='1B_task_RH-LH_early_error.png'):
    """
    Plots group-level early angular error for right learning and left transfer epochs,
    including significance stars for paired comparison.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with columns ['SubNo', 'Epoch', 'AngularError'].
    fig_name : str, optional
        Filename for the output plot.
    """
    epoch_order = ["rightlearning-early", "lefttransfer-early"]
    labels = ["RH Learning\n Early", "LH Transfer\n Early"]
    palette = ["orange", "green"]

    # Paired test (Pingouin)
    res = pg.pairwise_tests(
        data=early_error,
        dv='AngularError',
        within='Epoch',
        subject='SubNo'
    )
    if res.loc[0, "p-unc"] <= .01:
        pval_asterisks = '**'

    # Plot
    fig, ax = plt.subplots(figsize=(2.5, 6))
    sns.barplot(
        data=early_error, x='Epoch', y='AngularError', hue='Epoch',
        order=epoch_order, palette=palette, ax=ax, width=0.7
    )

    # Draw a line for significance and place asterisks above bars
    y_pos = 35
    ax.plot([0, 1], [y_pos, y_pos], color='k', linewidth=1.2)
    ax.text(0.5, y_pos + 1, pval_asterisks, ha='center', va='bottom', fontsize=18, fontweight='bold')
    # Format axes and labels
    ax.set(xticks=[0, 1], yticks=np.arange(0, 50, 10))
    ax.set_xticklabels(labels, fontsize=12, fontweight='bold', rotation=90)
    ax.set_ylabel('Angular error (°)', fontsize=12, fontweight='bold')
    ax.set_xlabel('')
    sns.despine(ax=ax)
    plt.tight_layout()
    
    fig.savefig(os.path.join(FIG_DIR, fig_name), dpi=300)

def main():

    data = pd.read_excel(os.path.join(DATA_DIR, '1B_data.xlsx'), sheet_name=None)

    plot_task_behaviour_binned(data['binned_learning_curve'])
    plot_early_error_change(data['rh_vs_lh_early_error'])
    
if __name__ == '__main__':
    main()