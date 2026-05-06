import random
from typing import Any

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import requests
from shapely.geometry import LineString, MultiLineString, Point, Polygon


def multiply(a, b):
    return a * b


def multiply_and_add(a, b, c):
    return a * b + c


def square_root(x):
    return x ** 0.5


def dice_roll():
    return random.randint(1, 6)


def load_featureserver_to_gdf(feature_server_url: str) -> gpd.GeoDataFrame:
    def arcgis_geometry_to_shapely(geometry: dict[str, Any] | None):
        if not geometry:
            return None

        if "x" in geometry and "y" in geometry:
            return Point(geometry["x"], geometry["y"])

        if "paths" in geometry:
            paths = geometry["paths"]
            if len(paths) == 1:
                return LineString(paths[0])
            return MultiLineString([LineString(path) for path in paths])

        if "rings" in geometry:
            rings = geometry["rings"]
            if not rings:
                return None
            shell = rings[0]
            holes = rings[1:] if len(rings) > 1 else None
            return Polygon(shell=shell, holes=holes)

        raise ValueError("Unsupported ArcGIS geometry format in response.")

    query_url = feature_server_url.rstrip("/") + "/0/query"
    page_size = 2000
    offset = 0
    all_rows: list[dict[str, Any]] = []

    while True:
        params = {
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "true",
            "f": "json",
            "resultOffset": offset,
            "resultRecordCount": page_size,
        }
        response = requests.get(query_url, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        if "error" in payload:
            message = payload["error"].get("message", "Unknown ArcGIS error")
            raise RuntimeError(f"ArcGIS query failed: {message}")

        features = payload.get("features", [])
        if not features:
            break

        for feature in features:
            attrs = feature.get("attributes", {}).copy()
            geom = feature.get("geometry")
            attrs["geometry"] = arcgis_geometry_to_shapely(geom)
            all_rows.append(attrs)

        offset += len(features)
        if len(features) < page_size:
            break

    df = pd.DataFrame(all_rows)
    if df.empty:
        return gpd.GeoDataFrame(df, geometry=[], crs="EPSG:3857")

    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:3857")
    return gdf


def plot_points_by_category(
    gdf: gpd.GeoDataFrame,
    column: str = "CONDITION",
    figsize: tuple[int, int] = (10, 10),
):
    if column not in gdf.columns:
        raise ValueError(f"Column '{column}' not found in GeoDataFrame.")

    plot_gdf = gdf.dropna(subset=["geometry"]).copy()
    if plot_gdf.empty:
        raise ValueError("GeoDataFrame has no valid geometry to plot.")

    ax = plot_gdf.plot(
        column=column,
        categorical=True,
        legend=True,
        figsize=figsize,
        markersize=10,
        alpha=0.8,
    )
    ax.set_title(f"Tree Points by {column}")
    ax.set_axis_off()
    plt.tight_layout()
    return ax



