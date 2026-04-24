"""
End-to-end ingestion, processing, and storage for Landsat-9 scenes.
"""

from pathlib import Path

import numpy as np
import odc.stac
import planetary_computer
import pystac_client

STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
BANDS = ["nir08", "red", "green", "blue", "qa_pixel", "lwir11"]
ZARR_ROOT = Path(__file__).parent.parent / "data" / "zarr"

_LST_SCALE = 0.00341802
_LST_OFFSET = 149.0
_KELVIN_OFFSET = 273.15


def search_scenes(bbox, datetime, max_cloud_cover=10):
    catalog = pystac_client.Client.open(
        STAC_URL,
        modifier=planetary_computer.sign_inplace,
    )
    search = catalog.search(
        collections=["landsat-c2-l2"],
        bbox=bbox,
        datetime=datetime,
        query={"eo:cloud_cover": {"lt": max_cloud_cover}},
    )
    return search.item_collection()


def load_scenes(items, bbox, chunks={"x": 256, "y": 256}):
    return odc.stac.stac_load(
        items, bands=BANDS, bbox=bbox, groupby="solar_day", chunks=chunks
    )


def mask_clouds(ds):
    cloud = (ds.qa_pixel & (1 << 3)) > 0
    shadow = (ds.qa_pixel & (1 << 4)) > 0
    return ds.where(~(cloud | shadow), np.nan).drop_vars("qa_pixel")


def add_lst_celsius(ds):
    ds["lst_celsius"] = ds["lwir11"] * _LST_SCALE + _LST_OFFSET - _KELVIN_OFFSET
    return ds


def add_ndvi(ds):
    nir = ds["nir08"].astype(float)
    red = ds["red"].astype(float)
    ds["ndvi"] = (nir - red) / (nir + red)
    return ds


def save_zarr(ds, name, mode="w-"):
    path = ZARR_ROOT / f"{name}.zarr"
    ds.to_zarr(path, mode=mode)
    return path


def run(bbox, datetime, name, max_cloud_cover=10):
    items = search_scenes(bbox, datetime, max_cloud_cover)
    ds = load_scenes(items, bbox).isel(time=0)
    ds = mask_clouds(ds)
    ds = add_lst_celsius(ds)
    ds = add_ndvi(ds)
    return save_zarr(ds, name)
