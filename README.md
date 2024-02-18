# CSR GRACE and GRACE-FO data in Google Earth Engine
This repository contains a set of function along with example scripts to preprocess and injest Gravity Recovery and Climate Experiment(GRACE) and GRACE follow on (GRACE-FO) dataset provided by [Center for Space Research (CSR)](https://www2.csr.utexas.edu/grace/RL06_mascons.html) at utexas. Subsequently, the full processing pipeline in this module is prepared for ground water change monitoring harnessing the power of Google Earth Engine.

The image injesting utilize the guideline based on Google Earth Engine [manifest uploads](https://developers.google.com/earth-engine/image_manifest).

![Grace Satellite Mascon](/assets/img/groundWater.gif)

<br>

## Workflow Overview
The workflow consists of following major steps:
    1. Downloading the CSR GRACE/GRACE-FO RL06.2 Mascon Grids w/ Corrections Applied dataset in `NetCDF` format from [Center for Space Research (CSR)](https://www2.csr.utexas.edu/grace/RL06_mascons.html).
    2. Extracting time property to a `CSV` using [xarray](https://docs.xarray.dev/en/stable/)
    3. Converting `NetCDF` data files to `GeoTiff` with [rioxarray](https://corteva.github.io/rioxarray/stable/)
    4. Mask out the ocean region to preserve underlying data only over the land surface. The mask algorithm utilizes <u>[`The Land and Ocean grids`](https://www2.csr.utexas.edu/grace/RL06_mascons.html)</u> that accompany the CSR RL06.2 Mascon Solution (v02).
    5. Upload the dataset to GCP bucket (manual)
    6. Creating image manifests (JSON-based files) describing the metadata and band names of the resulting Earth Engine asset
    7. Ingesting the dataset uploaded to GCP as assets into [Earth Engine](https://earthengine.google.com/) with [earth-engine-api](https://earthengine.google.com/) and [manifest uploads](https://developers.google.com/earth-engine/image_manifest)

<br>

![Workflow Diagram](/assets/img/Workflow.png)
<br>

### Overview of Analysis Ready Data(ARD) in GEE to user applications

![Application Diagram](/assets/img/application.png)

<br>

## Repository Contents:
* [`utils`](./utils/): all utilities scripts that can work in isolation to complete above steps.
  * [`01.timeUtils.py`](./utils/01.timeUtils.py): Generates a `CSV` file with `time metadata` and `ID` to identify the image.
  * [`02.grace_nc_to_masked_tif.py`](./utils/02.grace_nc_to_masked_tiff.py): Generates masked geotiff of land gravity measurements from `NetCDF` files.
  * [`03.gee_manifest_generator.py`](./utils/03.gee_manifest_generator.py): Generates `manifest.json` files, useful later to ingest using `earth-engine API`

* Example manifest files
  * [`20231101_20231130.json`](./20231101_20231130.json): Sample manifest file

<br>

## Python packages required
- [cftime](https://unidata.github.io/cftime/)
- [EarthEngine Python API](https://developers.google.com/earth-engine/python_install-conda.html)
- [xarray](http://xarray.pydata.org/en/stable/)
- [rioxarray](https://corteva.github.io/rioxarray/stable/)
- [geemap](https://geemap.org/)

<br>

## Cite this work
```
@misc{pyGRACE,
  author = {Hillson Ghimire},
  doi = {zenodo-placeholder},
  month = {02},
  title = {{GRACE Analysis Utility}},
  url = {https://github.com/hillsonghimire/pyGRACE},
  version = {1.0.0},
  year = {2024}
}
```

<br>

## References
1. 

<br>

## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

