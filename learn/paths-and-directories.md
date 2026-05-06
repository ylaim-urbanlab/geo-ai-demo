# Paths and Directories

A path is where a file should be saved or loaded from, and a directory is a folder in that path.

Most save functions can create a file, but they do not create missing parent folders automatically.

Why this matters here: saving to `out/denver_parkway_trees.shp` fails if the `out` folder does not already exist.
