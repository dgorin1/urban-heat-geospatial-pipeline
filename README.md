# Urban Heat Geospatial Pipeline

A scalable pipeline for processing and analyzing urban heat (thermal peril) data, with an initial focus on Boston. The goal is to ingest Landsat-9 satellite imagery via the STAC API, process it using a cloud-native geospatial stack (Xarray, Dask, Zarr), and produce spatially rigorous heat risk estimates that can scale to larger geographies.

This is early days — the project structure and core pipeline are actively being built out.

## Goals

- Ingest thermal infrared data from Landsat-9 via STAC API
- Store and process large raster datasets in Zarr format for scalability
- Integrate municipal boundary and land-use data from MassGIS
- Apply spatially independent train/test splits to avoid over-optimism in risk estimates
- Produce uncertainty-quantified, pixel-level heat risk outputs

## Tech Stack

| Layer | Tools |
|---|---|
| Data ingestion | STAC API, GDAL, Bash |
| Raster processing | Xarray, Dask, Zarr |
| Vector / analysis | GeoPandas, Scikit-Learn |
| Data sources | Landsat-9, MassGIS |
