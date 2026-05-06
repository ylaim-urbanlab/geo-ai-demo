# geo-ai-demo

Small Python workspace for pulling Denver tree data from an ArcGIS FeatureServer, exploring it in a GeoDataFrame, and saving exports locally. Learning notes live in `learn/`; shared helpers live in `src/`.

The walkthrough in the demo **glossed over environment setup** on purpose so the focus stayed on code and data. Below is enough detail for someone new to get a working Python stack.

## Layout

| Path | Purpose |
|------|---------|
| `src/` | Python modules (e.g. `tools.py`) |
| `notebooks/` | Jupyter notebooks |
| `learn/` | Short concept notes (functions, GeoDataFrames, exports, paths) |
| `out/` | Generated exports (gitignored; create the folder before saving) |
| `data/` | Local data / geodatabase (gitignored) |

See `context.md` for how you prefer to work (code in `/src`, run cells you paste yourself).

## Environment setup

### What you need

- **Python 3.12** (what this repo’s `requirements.txt` was frozen against). Older 3.10+ may work but is not what we tested.
- A way to manage packages without breaking your system Python.

You can install Python from [python.org](https://www.python.org/downloads/) and use `venv`, but **we recommend [Anaconda](https://www.anaconda.com/download)** or the smaller **[Miniconda](https://docs.conda.io/en/latest/miniconda.html)** so you get `conda` for isolated environments and fewer headaches with geospatial libraries.

### Option A — Anaconda or Miniconda (recommended)

1. **Install** Anaconda or Miniconda for your OS from the links above. During setup, allow the installer to initialize conda for your shell if it asks (makes `conda activate` work in the terminal).

2. **Open a new terminal** (so `conda` is on your `PATH`).

3. **Create a dedicated environment** with Python 3.12:

   ```bash
   conda create -n geo-ai-demo python=3.12 -y
   conda activate geo-ai-demo
   ```

4. **Go to the project folder** (the directory that contains `requirements.txt`):

   ```bash
   cd /path/to/geo-ai-demo
   ```

5. **Install pinned dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

6. **Register a Jupyter kernel** (optional but handy so the notebook can pick this env):

   ```bash
   python -m ipykernel install --user --name geo-ai-demo --display-name "Python (geo-ai-demo)"
   ```

7. **Start JupyterLab** when you want to work in the browser:

   ```bash
   jupyter lab
   ```

   In Cursor/VS Code, choose the **geo-ai-demo** interpreter or kernel for `notebooks/first_notebook.ipynb`.

### Option B — python.org + venv

1. Install Python 3.12 from [python.org](https://www.python.org/downloads/).
2. In the project folder:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

Geospatial wheels are usually available on PyPI for common platforms; if `pip install geopandas` fails, switch to Option A.

### Freezing dependencies again later

From an activated env that has everything you need:

```bash
pip freeze
```

Copy only the lines you want into `requirements.txt`. This repo keeps **PyPI-style** `package==version` pins so others are not stuck with `file://` URLs from conda’s internal builds.

## Notebook

Start with `notebooks/first_notebook.ipynb`. It loads the Denver parkway trees layer via `load_featureserver_to_gdf` in `src/tools.py` and explores plotting and exports.

### Demo note (path fix)

In an early demo recording, exports were written under `notebooks/out/`, which is easy to confuse with the project’s intended **`out/` at the repo root** (and can hit “folder does not exist” or clutter the notebook tree). The notebook now saves shapefiles with a path that goes up one level from the notebook folder, for example:

```python
gdf.to_file("../out/denver_parkway_trees.shp")
```

That matches the layout above and avoids the issue shown in the video. Ensure `out/` exists first (for example `Path("../out").mkdir(parents=True, exist_ok=True)` from a notebook in `notebooks/`).

## Git and large files

Exports (shapefiles, geodatabases) can be huge. They are listed in `.gitignore` so they are not committed. Do not commit multi-hundred-megabyte `.dbf` files; GitHub will reject pushes over its file size limit.
