# GeoDataFrame

A GeoDataFrame is a table (rows and columns) that also has a geometry column for spatial features.

It behaves like a pandas DataFrame, but with map-aware operations like plotting, spatial joins, and coordinate reference system (CRS) handling.

Why this matters here: the FeatureServer loader function returns a GeoDataFrame so you can inspect attributes and geometry in one object.

## Subsetting a GeoDataFrame

Subsetting means keeping only some rows or columns.

### Standard syntax (brackets)

Use brackets when you want clear, explicit filtering.

```python
# Keep only selected columns
gdf_subset_cols = gdf[["SPECIES_BO", "DIAMETER", "CONDITION", "geometry"]]

# Keep rows where one condition is true
gdf_good = gdf[gdf["CONDITION"] == "GOOD"]

# Keep rows where multiple conditions are true
gdf_big_good = gdf[(gdf["CONDITION"] == "GOOD") & (gdf["DIAMETER"] >= 20)]
```

### Query syntax (`.query`)

Use `.query()` when filter logic reads more naturally as a sentence.

```python
# Same logic using query syntax
gdf_good = gdf.query("CONDITION == 'GOOD'")

# Multiple conditions
gdf_big_good = gdf.query("CONDITION == 'GOOD' and DIAMETER >= 20")
```

Notes:
- Column names are written directly inside the query string.
- String values use quotes inside the string.
- If a column name has spaces, wrap it in backticks in query syntax.
