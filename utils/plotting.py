import os, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import natsort
import nibabel as nib
import cmasher as cmr
from brainspace.utils.parcellation import map_to_labels
from brainspace.mesh.mesh_io import read_surface
from surfplot import Plot
from surfplot.utils import add_fslr_medial_wall

from utils.config import *

plt.rcParams['font.family'] = ['Arial']
plt.rcParams["savefig.format"] = 'png'
plt.rcParams["savefig.dpi"] = 300

atlas_file = os.path.join(RESOURCES_DIR, 'Schaefer2018_400Parcels_17Networks_order.dlabel.nii')

def get_files(pattern, force_list=False):
    """Extracts files in alphanumerical order that match the provided glob 
    pattern.

    Parameters
    ----------
    pattern : str or list
        Glob pattern or a list of strings that will be joined together to form 
        a single glob pattern.  
    force_list : bool, optional
        Force output to be a list. If False (default), a string is returned in
        cases where only one file is detected.

    Returns
    -------
    str or list
        Detected file(s).

    Raises
    ------
    FileNotFoundError
        No files were detected using the input pattern.
    """
    files = natsort.natsorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError('Pattern could not detect file(s)')

    if (not force_list) & (len(files) == 1):
        return files[0] 
    else:
        return files
def _align_labels_to_atlas(x, source_labels, target_labels):
    """Match labels to corresponding vertex labels"""

    target = np.unique(target_labels)[1:]
    df1 = pd.DataFrame(target, index=target)
    df2 = pd.DataFrame(x, index=source_labels)
    return pd.concat([df1, df2], axis=1).iloc[:, 1:].values


def weights_to_vertices(data, target, labels=None):
    """Map weights (e.g., gradient loadings) to vertices on surface

    If `labels` is not specifiied, values in `data` are mapped to `target` in 
    ascending order.

    Parameters
    ----------
    data : numpy.ndarray or str
        Array containing region weights of shape (n_regions, n_features). If
        more than one feature/column is detected, then brain maps for each 
        feature are created. If a string, must be a valid CIFTI file name
    target : str
        CIFTI file name (dlabel or dscalar) that defines vertex-space for 
        mapping 
    labels : numpy.ndarray
        Numeric labels for each region (i.e. row of `data`) as they appear in 
        the atlas vertices. Required when `data` contains fewer regions than
        total regions in `target`, as is the case when `data` is a result of 
        some thresholded/indexing (e.g., `data` only contains weights of 
        significant regions). By default None.

    Returns
    -------
    numpy.ndarray
        Array of mapped vertices
    """
    if isinstance(target, str): 
        vertices = nib.load(target).get_fdata().ravel()
    else:
        vertices = target.ravel()
    #vertices = load_parcellation('schaefer', scale=400, join=True)

    if labels is not None:
        data = _align_labels_to_atlas(data, labels, vertices)

    mask = vertices != 0
    map_args = dict(target_lab=vertices, mask=mask, fill=np.nan)
    if (len(data.shape) == 1) or (data.shape[1] == 1):
        weights = map_to_labels(data.ravel(),  **map_args)
    else:
        weights = [map_to_labels(x, **map_args) for x in data.T]
    return weights

def get_surfaces(style='inflated', load=True):
    """Fetch surface files of a given surface style

    Parameters
    ----------
    style : str, optional
        Type of surface to return, by default 'inflated'

    Returns
    -------
    dict
        Dictionary of left (lh) and right (rh) surface files
    """

    surfaces = get_files(os.path.join(RESOURCES_DIR, f'*.{style}_*'))
    
    if load:
        surfs = [read_surface(i) for i in surfaces]
        return dict(zip(['lh', 'rh'], surfs))
    else:
        return surfaces

def get_sulc():
    """Get sulcal depth map for plotting style"""
    img = os.path.join(RESOURCES_DIR, 'S1200.sulc_MSMAll.32k_fs_LR.dscalar.nii')
    vertices = nib.load(img).get_fdata().ravel()
    return add_fslr_medial_wall(vertices)

def epoch_order():
    return {'rest': 1, 'leftbaseline': 2, 'rightbaseline': 3, 
             'rightlearning-early': 4, 'rightlearning-late': 5,
             'lefttransfer-early': 6, 'lefttransfer-late': 7,
             'baseline': 1, 'early': 2, 'late': 3,
             'left': 1, 'right': 2}


def pairwise_stat_maps(data, prefix, layercbar=False, dorsal=True, posterior=True, vmax='auto', 
                       vmin='auto', cbar_orientation='vertical', thresholded=True):
    """Plot pairwise comparisons t-maps on brain surfaces

    Parameters
    ----------
    data : pandas.DataFrame
        Pairwise t-test results
    prefix : str
        File name prefix
    dorsal : bool, optional
        Plot dorsal view, by default True
    posterior : bool, optional
        Plot posterior view, by default True
    vmax : float or str, optional
        Max value in colour range, by default 'auto'
    vmin : float or str, optional
        Min value in colour range, by default 'auto'
    cbar_orientation : str, optional
        Colour bar orientation, either 'vertical' or 'horizontal', 
        by default 'vertical'

    Returns
    -------
    matplotlib.figure.Figure
        Stat maps
    """
    pairwise_contrasts = data.groupby(['A', 'B'])
    list_ = []

    for name, g in pairwise_contrasts:
        # get stats of only significant regions
        sig = g[g['sig_corrected'].astype(bool)] if thresholded else g
        sig.set_index('roi_ix', inplace=True)
        if epoch_order()[name[0]] > epoch_order()[name[1]]:
            contrast = f'{name[0]}_{name[1]}'
            sig = sig[['T']]
        else:
            contrast = f'{name[1]}_{name[0]}'
            sig = -sig[['T']]
        sig = sig.rename(columns={'T': contrast + '_T'})
        list_.append(sig)
        
    df = pd.concat(list_, axis=1)

    # flip sign so that the second condition is the positive condition 
    # (because epochs are both alphabetical AND chronological, the 
    # positive condition is always the subsequent epoch)
    tvals = df.filter(like='T')
    
    cmap = cmr.get_sub_cmap('RdBu_r', .05, .95)

    surfaces = get_surfaces()
    sulc = get_sulc()

    sulc_params = dict(data=sulc, cmap='gray', cbar=False)
    layer_params = dict(cmap=cmap, cbar=layercbar, color_range=(-vmax, vmax))
    outline_params = dict(cbar=False, cmap='binary', as_outline=True)

    for i in tvals.columns:
        contrast = i[:-2].replace('_', '_vs_')
        x = weights_to_vertices(tvals[i], atlas_file, 
                                           tvals.index.values)
        # row 
        p = Plot(surfaces['lh'], surfaces['rh'], layout='row', 
                 mirror_views=True, size=(800, 200), zoom=1.2)
        p.add_layer(**sulc_params)
        p.add_layer(x, **layer_params)
        p.add_layer((np.nan_to_num(x) != 0).astype(float), **outline_params)
        fig = p.build()
        fig.savefig(prefix + contrast)

        if dorsal:
            p = Plot(surfaces['lh'], surfaces['rh'], views='dorsal', 
                    size=(150, 200), zoom=3.3)
            p.add_layer(**sulc_params)
            p.add_layer(x, **layer_params)
            p.add_layer((np.nan_to_num(x) != 0).astype(float), **outline_params)
            fig = p.build(colorbar=False)
            fig.savefig(prefix + contrast + '_dorsal')

        if posterior:
            p = Plot(surfaces['lh'], surfaces['rh'], views='posterior', 
                    size=(150, 200), zoom=3.3)
            p.add_layer(**sulc_params)
            p.add_layer(x, **layer_params)
            p.add_layer((np.nan_to_num(x) != 0).astype(float), **outline_params)
            fig = p.build(colorbar=False)
            fig.savefig(prefix + contrast + '_posterior')

    return fig
