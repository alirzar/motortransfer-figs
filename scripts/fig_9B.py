"""
Script to visualize behavioral angle distributions for each subject and condition (Figure 9B).

This script:
- Loads behavioral angle data from '9B_data.xlsx'.
- Plots distributions for right-hand early, left-hand early, and transfer
- Saves the resulting three-panel figure to the FIG_DIR directory.
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

def plot_distribution(df, angle, ax):
    """
    Plot the distribution of a specified angle variable as a boxplot with overlaid scatter for individual values.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing subject and angle data.
    angle : str
        Name of the column in df corresponding to the angle to plot.
    ax : matplotlib.axes.Axes
        The axes on which to plot.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes with the plot.
    """
    plot_df = df.copy()
    plot_df['x'] = 1
    box_line_color = 'k'
    sns.boxplot(x='x', y=angle, data=plot_df, color='silver', 
                boxprops=dict(edgecolor=box_line_color), 
                medianprops=dict(color=box_line_color),
                whiskerprops=dict(color=box_line_color),
                capprops=dict(color=box_line_color),
                showfliers=False, width=.5, ax=ax)
    
    np.random.seed(1)
    jitter = np.random.uniform(.01, .4, len(plot_df['x']))
    ax.scatter(x=plot_df['x'] + jitter , y=plot_df[angle], 
               c='k', ec='k', linewidths=1, s=10,
               clip_on=False)

    ax.set(xticks=[], 
           yticks=np.arange(-15, 60, 15))
    sns.despine(bottom=True)
    return ax

def main():

    data = pd.read_excel(os.path.join(DATA_DIR, '9B_data.xlsx'))
    
    fig, axs = plt.subplots(1, 3, figsize=(6, 4))
    angle_names = ['RH Early', 'LH Early', 'Transfer']
    titles = ['RH', 'LH', '']
    ylabels = ['Early Error (°)', 'Early Error (°)', 'Transfer (°)']

    for i, (ax, angle, title, ylabel) in enumerate(zip(axs, angle_names, titles, ylabels)):
        plot_distribution(data[['sub', angle]], angle, ax)
        ax.axhline(0, lw=1, c='k', ls='--')
        ax.set_title(title, fontsize=18)
        ax.set(xlabel='', ylabel=ylabel)
        ax.yaxis.label.set_size(16) 
    plt.subplots_adjust(wspace=1.3)
    
    fig.savefig(os.path.join(FIG_DIR, '9B_behaviour_distributions.png'), dpi=300)
    
if __name__ == '__main__':
    main()