"""
Script to visualize model comparison for representational similarity analysis (RSA) (Figure 3E).

This script:
- Loads RSA model evaluation results from '3E_data.xlsx'.
- Generates bar plots summarizing the performance and significance of different RSA models.
- Saves the final figure to the FIG_DIR directory.
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

def plot_rsa_model_comparisons(data, fig_name='3E_rsa_models_comparison.png'):
    """
    Plot model comparison for RSA analysis.

    Parameters
    ----------
    data : dict
        Dictionary containing 'evaluations', 'models_summary', and 'models_comparison_fdr' DataFrames.
    fig_name : str
        Name of the figure file to save.
    """
    # Extract relevant data
    boot_df = data['evaluations']
    pvals_zero = data['models_summary']['p_0'].values
    pvals_nc = data['models_summary']['p_NC'].values
    pairwise_qvals = data['models_comparison_fdr'].iloc[:, 1:].values
    model_names = list(boot_df.columns)
    # Plot settings
    colors = ['green', 'orange', 'blue', 'red']
    n_models = len(model_names)
    means = boot_df.mean(axis=0)
    sems = boot_df.std(axis=0)


    x = np.arange(len(model_names))
    fig, ax = plt.subplots(figsize=(4, 4))
    bars = ax.bar(x, means, yerr=sems, capsize=3, color=colors)
    
    # Significance vs zero (white circle at y=0)
    for i, p in enumerate(pvals_zero):
        if p < 0.05:
            ax.plot(x[i], 0, marker="o", markersize=8, color="white", markeredgecolor="k", zorder=10)
    
    # Significance vs noise ceiling (gray triangle at y=1)
    for i, p in enumerate(pvals_nc):
        if p < 0.05:
            ax.plot(x[i], 1, marker="v", markersize=8, color="lightgray", markeredgecolor="k", zorder=10)
    
    # Pairwise significant comparisons (FDR corrected)
    k = 1
    for i in range(n_models):
        for j in range(i+1, n_models):
            if pairwise_qvals[i, j] < 0.05:
                y = 1 - .06 * k
                ax.plot([x[i], x[j]], [y, y], color='k', linewidth=1.5)
                ax.text((x[i]+x[j])/2, y, '**', ha='center', va='bottom', fontsize=12)
                k += 1
    
    ax.set_xticks(x)
    ax.set_xticklabels(model_names)
    ax.set_ylabel("Cosine Similarity")
    plt.tight_layout()
    sns.despine()
    fig.savefig(os.path.join(FIG_DIR, fig_name), dpi=300)
    return
def main():

    data = pd.read_excel(os.path.join(DATA_DIR, '3E_data.xlsx'), sheet_name=None)

    plot_rsa_model_comparisons(data)
    
if __name__ == '__main__':
    main()