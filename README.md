# svgTojson
This project aims to parse a svg file into a json file. It will only convert `path` and `rect` objects in the SVG images.

The converter converts each `path` and `rect` 
from the `SVG` file into the following format:

```bash
points = [[0, 1], [0, 5]...]
edges  = [[0, 1, 0], [1, 2, 0]...[30,54,7]]
edge_chain_ids = [0, 1, 2, ... M]
labels = ['wall-face-drywall', ... 'wall-face-drywall']
```

Wherein:
- `points` is a list of all *unique* `x`, and `y` coordinates of `path` and `rect` points (no duplicate points allowed), size `Nx2`
- `edges` is a list of all `start_point_id`, `end_point_id`, `edge_chain_id` for all unique edges in the `SVG` file, size `Mx2`
- `edge_chain_id` is a list of all unique edge chain id's; wherein an edge chain id is define as a single continuous `path` or `rect`; i.e. a rectangle would have one chain id for all of its 4 edges. These id's fill the 3rd item in `edges`, size `Kx1`
- `labels` is a list of the associated group id's from the SVG using the `id` field mapped 1:1 to each edge. I.E. edge 0 might be of type `face-wall-drywall`. The `labels` list is the same size as the `edges` list, `Mx1`

An example SVG and associated JSON file are provided in `example/test_svg.svg` and `example/my_out.json`.

1. Install pip dependencies

```bash
python3 -m pip install -r requirements.txt
```
2. Usage

There are two ways to run the convertor. You can `import convertor from driver` and use 

```bash
convert(<path/to/svg/file>, <path/to/json/file>)
```

Or it can get executed from command line with the following command. 

```
python driver.py --file_in <path/to/svg/file> --file_out <path/to/json/file>
```

Here is an example for its usage which produces the example json file.
```
python driver.py --file_in test_svg.svg --file_out my_out.json
```

