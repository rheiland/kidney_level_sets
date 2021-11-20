# kidney_level_sets

## Goal: construct a distance function (in C++) that can find the shortest distance from any point in our domain to one of the boundaries of these 4 structures.
Open an SVG file in your browser, e.g., `file:///Users/heiland/git/kidney_level_sets/data/endo_cells.svg`

<img src="image_proc/endo_cells_screen.png" alt="original" height="300">

---
## Process SVG geometry to extract boundary points

```
cd python
python cells_pts.py ../data/endo_cells.svg
```
<img src="images/endo_pts.png" alt="endo pts" height="300">


---
## Failed experiment with image-based approach (and scikit-image)

<img src="image_proc/endo_eroded.png" alt="eroded/capped" height="300"><img src="image_proc/endo_eroded_fill.png" alt="filled" height="300">

---

```
cd image_proc
python endo_skeleton.py
```

<img src="images/skeleton_1x2.png" alt="skeleton" height="500">
