"""
Script to visualize eccentricity patterns for all seed regions during all epochs (Figure 8).

This script:
- Loads region eccentricity data for all seeds from '8_data.xlsx'.
- Plots the distribution and mean eccentricity for each seed region and epoch
- Saves the resulting figure to the FIG_DIR directory.
"""
import os
import sys
import pandas as pd
import seaborn as sns

# Ensure project root is in sys.path for absolute imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.config import FIG_DIR, DATA_DIR
os.makedirs(FIG_DIR, exist_ok=True)

def plot_seed_eccentricity(ecc_data, fig_name='8_seeds_eccentricity.png'):
    '''
    plot eccentricity pattern for all seed regions during all epochs for 
    all subjects
    
    Parameters
    ----------
    ecc_data : Pandas DataFrame 
        with eccentrity column for all rois and all subjects 
        and all the existing epochs in the experiment.
    fig_name : str
        Name of the figure file to save.
    Returns
    -------
    plot of eccentricity pattern and mean eccentricity for input seeds.

    '''
    # Epoch ordering and color palette
    epoch_color_map = {
        'leftbaseline': 'orange',
        'rightbaseline': 'green',
        'rightlearning-early': 'green',
        'rightlearning-late': 'green',
        'lefttransfer-early': 'orange',
        'lefttransfer-late': 'orange'
    }
    ecc_data = pd.concat(ecc_data, names=['seed']).reset_index().drop(columns=['level_1', 'roi'])
    epoch_order = list(epoch_color_map.keys())
    labels = ['LH Baseline', 'RH Baseline', 'RH Learning Early',
              'RH Learning Late', 'LH Transfer Early', 'LH Transfer Late']
    cmap = list(epoch_color_map.values())
    ecc_data['epoch'] = pd.Categorical(ecc_data['epoch'], categories=epoch_order, ordered=True)
    ecc_data.sort_values('epoch', inplace=True)
    ecc_data.reset_index(drop=True, inplace=True)
    g = sns.FacetGrid(data=ecc_data, col_wrap=2, col='seed',
                      height=2.5, sharey=False,
                      col_order=['Left M1', 'Right M1', 'Left mPFC', 'Right mPFC'])
    g.map_dataframe(sns.lineplot, x='epoch', y='distance', errorbar=None, 
                    marker='o', ms=6, lw=1.2, mfc='w', mec='k', color='k')
    g.map_dataframe(sns.stripplot, x='epoch', y='distance', jitter=.1, 
                    zorder=-1, s=4, alpha=.5, palette=cmap, hue='epoch')
    g.set_axis_labels('', "Eccentricity")
    g.set_xticklabels(labels, rotation=90)
    for ax, title in zip(g.axes.flat, g.col_names):
        ax.set_title(title.replace('roi = ', ''))
    g.savefig(os.path.join(FIG_DIR, fig_name), dpi=300)
    
def main():

    data = pd.read_excel(os.path.join(DATA_DIR, '8_data.xlsx'), sheet_name=None)

    plot_seed_eccentricity(data)
    
if __name__ == '__main__':
    main()