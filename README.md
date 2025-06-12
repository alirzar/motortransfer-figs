# motortransfer - figures
Data and code for Rezaei et al., 2025 (PLOS Biology).

Dependencies: numpy, pandas, matplotlib, seaborn, scipy, openpyxl, nibabel, brainspace, surfplot, cmasher, natsort.  
## Environment setup:  
```
git clone https://github.com/alirzar/motortransfer-figs
cd motortransfer-figs/
conda env create -f environment.yml  
conda activate motortransfer-figs
```
## To generate all figures:
```
python main.py
```

### Folders:
- data/         Input data and resources (Excel files, surface/atlas files)
- figures/      Output figures (auto-generated)
- scripts/      Python scripts for each figure
- utils/        Shared plotting/configuration code

All required data files are in `data/`.  
All generated figures are saved in `figures/`.