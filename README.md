# HiRISE Unfiltered Multispectral Cube Processing Pipeline

## Overview

This repository provides an open-source Python implementation for processing, dark subtraction correction with quality assessment of NASA Mars Reconnaissance Orbiter (MRO) High Resolution Imaging Science Experiment (HiRISE) Unfiltered multispectral observations.

The pipeline was developed to enable reproducible and batch processing of HiRISE multispectral datasets for quantitative spectral analysis, particularly for studies requiring accurate characterization of subtle radiometric differences between HiRISE color bands.

The processing methodology, including detailed descriptions of the dark subtraction methodology, validation procedures, and scientific application are described in:

Rangarajan, V.G., Tornabene, L.L., Osinski, G.R., Dundas, C.M., Beyer, R.A., Herkenhoff, K.E., Byrne, S., Heyd, R., Seelos, F.P., Munaretto, G., Dapremont, A., 2024. Novel quantitative methods to enable multispectral identification of high-purity water ice exposures on Mars using High Resolution Imaging Science Experiment (HiRISE) images. Icarus, 419, 115849. https://doi.org/10.1016/j.icarus.2023.115849 

This pipeline requires input of UNFILTERED HiRISE COLOR products converted to .tif using GDAL. The detailed procedure for generating UNFILTERED HiRISE ISIS cubes as well as their conversion to .tif is provided in the supplementary material in Rangarajan et al. (2024).

---

# Features

The pipeline provides:

- Automated HiRISE UNFILTERED product ingestion
- Dark pixel identification
- Dark subtraction correction
- Quality control visualization products
- Multispectral band reordering
- ENVI-compatible output generation
- Batch processing of multiple HiRISE observations
- Automated processing summaries and failure reporting

---

# Processing Workflow

The processing chain follows:

```
HiRISE COLOR4 image
        |
        v
Image and metadata ingestion
        |
        v
Invalid pixel masking
        |
        v
Dark pixel identification
        |
        v
Dark subtraction correction
        |
        v
Quality control assessment
        |
        v
Band ordering correction
        |
        v
ENVI product generation
```

---

# Input Data

The pipeline accepts HiRISE UNFILTERED products in TIF format.

Example:

```
ESP_053039_1640_UNFILTERED_COLOR4.tif
```

Native HiRISE COLOR4 detector ordering:

| Native band | Detector channel |
|---|---|
| Band 1 | Near Infrared |
| Band 2 | Red |
| Band 3 | Blue-Green |

---

# Output Products

## Quality Control Products

QC products are generated as PNG images and include:

- detected dark pixel locations
- dark minima statistics
- correction diagnostics
- before/after comparisons

Example:

```
qc/

ESP_053039_1640_dark_QC.png

ESP_053039_1640_DS_QC.png
```

---

## Dark Subtraction Corrected ENVI Products

Corrected products are exported in ENVI format:

```
corrected/

ESP_053039_1640_DS_CORRECTED.img

ESP_053039_1640_DS_CORRECTED.hdr
```

The products are compatible with:

- ENVI
- QGIS
- Python spectral analysis tools
- other ENVI-compatible planetary science software

---

# Final Band Ordering

The exported science products are reordered into multispectral interpretation order:

| Output band | Band name | Central wavelength (nm) |
|---|---|---|
| Band 1 | BlueGreen | 502.56015 |
| Band 2 | Red | 691.897644 |
| Band 3 | NearInfrared | 873.403381 |

This differs from the native detector ordering obtained from ISIS.

---

# NoData Handling

During processing, invalid pixels are represented internally as:

```
NaN
```

During ENVI export, invalid pixels are converted to:

```
65535
```

and recorded in the ENVI header as:

```
data ignore value = 65535
```

---

# Batch Processing

The pipeline supports processing of multiple HiRISE observations.

Example input directory:

```
input/

ESP_053039_1640_UNFILTERED_COLOR4.tif
ESP_053040_1640_UNFILTERED_COLOR5.tif
ESP_053041_1640_UNFILTERED_COLOR4.tif
```

Batch processing automatically:

- processes each observation sequentially
- generates QC products
- exports corrected ENVI products
- records processing status

---

# Quality Control and Failure Handling

The pipeline performs validation checks before applying dark subtraction correction.

If physically invalid dark minima values are detected:

```
DS correction not possible - negative minima values
```

the observation is rejected and processing continues with subsequent observations.

Failure reasons are recorded in the batch summary CSV.

Example statuses:

```
SUCCESS

FAILED_DS_NEGATIVE_MINIMA

FAILED_ERROR
```

---

# Installation

## Python Environment

The recommended environment is:

```
python-processing
```

Required packages include:

- Python 3.x
- numpy
- matplotlib
- tifffile
- spectral
- pillow

An environment file (`environment.yml`) is provided for reproducible installation.

---

# Running the Pipeline

Processing is performed through Jupyter notebooks.

Example workflow:

1. Activate the Python environment:

```
python-processing
```

2. Open:

```
Run_HiRISE_Processing.ipynb
```

3. Define input/output locations:

```python
input_folder = "/path/to/HiRISE/input"

qc_folder = "/path/to/HiRISE/qc"

corrected_folder = "/path/to/HiRISE/corrected"
```

4. Execute the processing workflow.

---

# Repository Structure

```
HiRISE_Python/

├── hirisepy/
│   ├── pipeline.py
│   ├── batch.py
│   ├── visualization.py
│   ├── dark_correction.py
│   ├── band_stacking.py
│   └── envi_io.py
│
├── notebooks/
│   └── Run_HiRISE_Processing.ipynb
│
├── environment.yml
│
├── README.md
│
└── LICENSE
```

---

# Citation

If you use this software or methodology in scientific work, please cite:

Rangarajan, V.G., Tornabene, L.L., Osinski, G.R., Dundas, C.M., Beyer, R.A., Herkenhoff, K.E., Byrne, S., Heyd, R., Seelos, F.P., Munaretto, G., Dapremont, A., (2024). Novel quantitative methods to enable multispectral identification of high-purity water ice exposures on Mars using High Resolution Imaging Science Experiment (HiRISE) images. Icarus, 419, 115849. https://doi.org/10.1016/j.icarus.2023.115849

---

# License

A license file will be included with this repository.

Please consult the license terms before redistribution or modification.

---

# Acknowledgements

This work utilizes data from NASA's Mars Reconnaissance Orbiter High Resolution Imaging Science Experiment (HiRISE).

The authors acknowledge the HiRISE science team and the planetary science community for maintaining publicly available Mars orbital datasets.