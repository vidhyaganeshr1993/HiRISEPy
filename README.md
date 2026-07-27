# HiRISEPy: Python-Based Processing Pipeline for NASA MRO HiRISE Unfiltered Multispectral Data

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21628753.svg)](https://doi.org/10.5281/zenodo.21628753)

## Overview

This repository provides an open-source Python implementation for processing, dark subtraction correction with quality assessment of NASA Mars Reconnaissance Orbiter (MRO) High Resolution Imaging Science Experiment (HiRISE) Unfiltered multispectral observations.

The pipeline was developed to enable reproducible and batch processing of HiRISE multispectral datasets for quantitative spectral analysis, particularly for studies requiring accurate characterization of subtle radiometric differences between HiRISE color bands.

The processing methodology, including detailed descriptions of the dark subtraction methodology, validation procedures, and scientific application are described in:

Rangarajan, V.G., Tornabene, L.L., Osinski, G.R., Dundas, C.M., Beyer, R.A., Herkenhoff, K.E., Byrne, S., Heyd, R., Seelos, F.P., Munaretto, G., Dapremont, A., 2024. Novel quantitative methods to enable multispectral identification of high-purity water ice exposures on Mars using High Resolution Imaging Science Experiment (HiRISE) images. Icarus, 419, 115849. https://doi.org/10.1016/j.icarus.2023.115849 

## Scientific Background

HiRISE COLOR observations provide three-channel visible-near infrared measurements of the Martian surface. However, quantitative spectral analysis requires careful treatment of band and scene-dependent effects due to atmospheric scattering.

HiRISEPy implements a dark subtraction correction approach designed to mitigate effects of atmospheric scattering using the darkest measurable pixels within each observation. The corrected products preserve the original calibrated radiometric information while improving our estimation of surface spectral behaviour.

The software is intended for users performing quantitative analysis of HiRISE multispectral observations rather than simple image visualization.

---

# Features

The pipeline provides:

## Data Processing

- Automated ingestion of HiRISE UNFILTERED COLOR observations
- Metadata extraction from input products
- Invalid pixel masking
- Automated dark pixel identification
- Automated dark pixel spectral validation prior to correction
- Dark subtraction correction
- Multispectral band reordering
- ENVI-compatible output generation

## Quality Assessment

HiRISEPy includes automated quality assessment before and after dark subtraction correction.

Diagnostic products include:

- dark pixel location maps
- dark minima statistics
- dark pixel spectral plots
- before/after correction comparisons
- automated QC reports
- batch processing summaries

Before applying dark subtraction, HiRISEPy evaluates the physical validity and spectral consistency of the automatically selected dark pixels.

The QC system includes:

- **Negative minima detection**
    - Dark subtraction is aborted if any automatically selected minimum spectrum contains negative I/F values.

- **Dark spectrum consistency assessment**
    - The three independently selected minimum pixels are compared using pairwise spectral RMSE.
    - If the spectral difference exceeds the defined threshold, a warning is generated.
    - Warning cases continue processing but are flagged in the batch summary output.


## Batch Processing

Batch processing automatically:

- processes each observation sequentially
- generates QC products
- exports corrected ENVI products
- records processing status and QC information

Each observation is processed independently. If an individual observation fails, the failure is recorded and processing continues with subsequent datasets.

The batch summary CSV provides an audit record containing:

- filename
- processing status
- QC messages
- observation metadata
- automatically selected dark pixel I/F values

---

# Processing Workflow

The processing chain follows:

```
HiRISE UNFILTERED COLOR observation
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
Dark spectrum extraction
        |
        v
Negative minima validation
        |
        +-----------------------------+
        |                             |
        v                             v
 Negative minima detected        No negative minima
        |                             |
        v                             v
     Abort                 Spectral consistency check
                                      |
                                      +----------------------+
                                      |                      |
                                      v                      v
                              RMSE acceptable        RMSE above threshold
                                      |                      |
                                      v                      v
                                  SUCCESS              WARNING
                                      |                      |
                                      +-----------+----------+
                                                  |
                                                  v
                                  Dark subtraction correction
                                                  |
                                                  v
                                  QC product generation
                                                  |
                                                  v
                                  Band re-ordering
                                                  |
                                                  v
                                  ENVI output generation

```
---

# Supported Input Data

HiRISEPy currently requires:

ISIS-processed HiRISE Unfiltered cubes converted to TIFF format using GDAL

Example:

ESP_053039_1640_UNFILTERED_COLOR4.tif

The procedure for generating ISIS UNFILTERED products and converting them to TIFF format is described in the supplementary material of Rangarajan et al. (2024).

## Native HiRISE products detector band ordering:

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

## Dark Pixel Validation

Before correction, the automatically selected dark pixels are evaluated for physical validity and spectral consistency.

### Negative minima check

If any selected dark spectrum contains negative I/F values:

```
DS correction not possible - negative minima values
```

the observation is rejected because the selected dark pixels are considered physically invalid for dark subtraction correction.

Processing continues with subsequent observations during batch processing.

### Dark spectral consistency check

The three independently selected minimum pixels are compared using pairwise spectral RMSE.

If the maximum RMSE exceeds the defined threshold, the observation is flagged:

```
WARNING: Dark spectra RMSE exceeds threshold. Please verify DS correction results.
```

Warning cases continue through dark subtraction correction, but the QC status is recorded in the batch summary CSV.

Example statuses:

```
SUCCESS
WARNING
FAILED_DS_NEGATIVE_MINIMA
FAILED_ERROR
```

---

# Installation

## Python Environment

Required packages include:

- Python 3.x
- numpy
- matplotlib
- tifffile
- spectral
- pillow

---

# Running the Pipeline

Processing is performed through Jupyter notebooks.

Example workflow:

1. Activate the Python environment:

```
conda activate "your-environment-name"
```

2. Open the provided Jupyter notebook:

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
│   ├── __init__.py
│   ├── dark_correction.py
│   ├── dark_pixels.py
│   ├── io.py
│   ├── masking.py
│   ├── metadata.py   
│   ├── quality_control.py
│   └── envi_io.py
│
├── notebooks/
│   └── Run_HiRISE_Processing.ipynb
│
├── README.md
│
└── LICENSE
```

---

# Software Architecture

HiRISEPy is organized into modular Python components, with each module responsible for a specific stage of the processing workflow.

## Module Description

### `pipeline.py`

Core processing workflow module.

This module defines the primary HiRISE processing pipeline and coordinates the sequential execution of individual processing steps:

- Input image loading
- Metadata extraction
- Invalid pixel masking
- Dark pixel identification
- Dark spectrum extraction and validation
- Dark subtraction correction
- Band reordering
- Output generation
- Quality control product creation

The pipeline module provides the main interface for processing individual HiRISE observations.


---

### `batch.py`

Batch processing and automation module.

This module enables processing of multiple HiRISE observations without manual intervention.

Functions include:

- Iterating through directories containing HiRISE observations
- Executing the processing pipeline for each observation
- Generating standardized outputs
- Recording successful and failed processing attempts
- Producing processing summaries

This module is designed for large-scale processing campaigns involving multiple HiRISE observations.


---

### `dark_correction.py`

Dark subtraction correction module.

This module implements the radiometric correction methodology described in Rangarajan et al. (2024).

Functions include:

- Applying dark subtraction correction for each band
- Estimating dark signal contributions
- Generating corrected multispectral products
- Supporting before/after correction validation

The correction preserves the calibrated HiRISE radiometric information while reducing detector-dependent offsets.


---

### `dark_pixels.py`

Dark pixel identification module.

This module identifies candidate dark pixels within HiRISE observations for use in dark subtraction correction.

Functions include:

- Searching individual detector channels
- Identifying minimum radiance/I/F locations
- Recording pixel coordinates and values
- Providing dark pixel statistics for quality assessment

---

### `quality_control.py`

Dark spectrum validation module.

This module evaluates the physical validity and spectral consistency of automatically selected dark pixels before dark subtraction correction.

Functions include:

- Detecting negative dark spectrum values
- Calculating pairwise spectral RMSE
- Assigning SUCCESS, WARNING, or FAILED QC states
- Providing quality metrics for batch processing summaries

---

### `masking.py`

Invalid pixel handling module.

This module manages invalid or unusable pixels during processing.

Functions include:

- Identifying NoData regions
- Applying invalid pixel masks
- Preventing corrupted pixels from influencing correction calculations
- Maintaining NaN-based internal data representation


---

### `metadata.py`

HiRISE metadata extraction module.

This module extracts and stores observation-level metadata required for processing and interpretation.

Information includes:

- Observation identifiers
- Image dimensions
- Number of spectral bands
- Band descriptions
- Wavelength information


---

### `band_stacking.py`

Multispectral band organization module.

This module manages HiRISE COLOR band ordering and creates analysis-ready multispectral data products.

Functions include:

- Correcting native detector ordering
- Rearranging bands into spectral interpretation order
- Generating stacked multispectral arrays


---

### `envi_io.py`

ENVI input/output module.

This module provides functions for reading and writing ENVI-compatible products.

Functions include:

- Generating ENVI `.hdr` metadata files
- Exporting corrected image cubes
- Maintaining wavelength information
- Preserving NoData definitions

Generated products are compatible with ENVI, QGIS, and other planetary remote sensing software.


---

### `visualization.py`

Quality control and visualization module.

This module generates diagnostic products used for evaluating processing performance.

Functions include:

- HiRISE false-colour image generation
- Contrast stretching for visualization
- Dark pixel location visualization
- Spectral plotting
- Before/after correction comparisons
- Automated QC report generation

All visualization operations are independent of the scientific pixel values and do not modify the underlying calibrated data.


---

### `io.py`

General input/output utility module.

This module provides supporting functions for:

- File handling
- Data loading utilities
- Directory management
- Common processing operations shared across modules

---


# Development Philosophy

HiRISEPy follows a modular design where individual processing steps are separated into independent components.

This approach provides:

- Improved reproducibility
- Easier maintenance
- Transparent scientific workflows
- Simplified extension for future HiRISE processing applications

---


# Citation

If you use this software or methodology in scientific work, please cite:

Software: 
Rangarajan, V.G. (2026). HiRISEPy: A Python-Based Processing Pipeline for NASA MRO HiRISE Unfiltered Multispectral Data. Zenodo. https://doi.org/10.5281/zenodo.21628753. 

Methodology: 
Rangarajan, V.G., Tornabene, L.L., Osinski, G.R., Dundas, C.M., Beyer, R.A., Herkenhoff, K.E., Byrne, S., Heyd, R., Seelos, F.P., Munaretto, G., Dapremont, A., (2024). Novel quantitative methods to enable multispectral identification of high-purity water ice exposures on Mars using High Resolution Imaging Science Experiment (HiRISE) images. Icarus, 419, 115849. https://doi.org/10.1016/j.icarus.2023.115849

---

# Acknowledgements

This work utilizes data from NASA's Mars Reconnaissance Orbiter High Resolution Imaging Science Experiment (HiRISE).

The author acknowledges the HiRISE science team for maintaining publicly available HiRISE datasets.
