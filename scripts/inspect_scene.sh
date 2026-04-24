#!/usr/bin/env bash
# Inspect a Landsat scene's metadata and band info using GDAL CLI tools.
# Usage: ./scripts/inspect_scene.sh <path/to/scene.tif>
#
# What each command tells you:
#   gdalinfo          → projection, bounding box, pixel size, band count, data type
#   gdalinfo -stats   → min/max/mean/stddev of pixel values (forces a full scan)
#   gdalinfo -hist    → pixel value histogram (good for spotting cloud contamination)

set -euo pipefail

SCENE=$1

echo "=== Basic metadata ==="
gdalinfo "$SCENE"

echo ""
echo "=== Band statistics ==="
gdalinfo -stats "$SCENE"

echo ""
echo "=== Histogram ==="
gdalinfo -hist "$SCENE"
