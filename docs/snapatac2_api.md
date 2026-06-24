# API Documentation

## snapatac2.concat

Source module: `snapatac2._snapatac2`

Signature:

```python
snapatac2.concat(adatas, *, join='inner', label=None, keys=None, file=None, backend=None)
```

Docstring:

```text
Concatenates AnnData objects.

When `file` is provided, this function saves the merged AnnData object on disk
in a streaming fashion. This is memory efficient and allows merging large datasets
that do not fit into memory.

Parameters
----------

adatas: list[AnnData]
    List of AnnData objects to concatenate.
join: Literal['inner', 'outer']
    How to handle observations and variables that are not shared between all AnnData objects.
label: str | None
    Column in axis annotation (i.e. .obs or .var) to place batch information in. If it’s None, no column is added.
keys
    Names for each object being added. These values are used for column values for label.
file: Path | None
    If provided, the concatenated AnnData will be saved to this file.
backend: Literal['hdf5', 'zarr']
    Backend to use for writing the output file.

Returns
-------

AnnData
    The concatenated AnnData object.

See Also
--------
AnnDataSet
```

## snapatac2.get_write_options

Source module: `snapatac2._snapatac2`

Signature:

```python
snapatac2.get_write_options()
```

Docstring:

```text
Get the current default write configuration.

Returns the thread-local default configuration used for dataset writes.

Returns
-------
dict
    Dictionary with keys "compression" and "block_size".

Examples
--------
>>> import anndata_rs
>>> config = anndata_rs.get_write_options()
>>> print(config["compression"])
Compression.zstd(5)
>>> print(config["block_size"])
None
```

## snapatac2.read

Source module: `snapatac2._snapatac2`

Signature:

```python
snapatac2.read(filename, backed='r+', backend=None)
```

Docstring:

```text
Read `.h5ad`-formatted hdf5 file.

Parameters
----------

filename: Path
    File name of data file.
backed: Literal['r', 'r+'] | None
    Default is `r+`.
    If `'r'`, the file is opened in read-only mode.
    If `'r+'`, the file is opened in read/write mode.
    If `None`, the AnnData object is read into memory.
backend: Literal['hdf5', 'zarr']
```

## snapatac2.read_10x_mtx

Source module: `snapatac2._io`

Signature:

```python
snapatac2.read_10x_mtx(path: 'Path', file: 'Path | None' = None, prefix: 'str | None' = None) -> 'AnnData'
```

Docstring:

```text
Read 10x-Genomics-formatted mtx directory.

Parameters
----------
path
    Path to directory for `.mtx` and `.tsv` files. The directory should contain
    three files:

    1. count matrix: "matrix.mtx" or "matrix.mtx.gz".
    2. features: "genes.tsv", or "genes.tsv.gz", or "features.tsv", or "features.tsv.gz".
    3. barcodes: "barcodes.tsv", or "barcodes.tsv.gz".
file
    File name of the ".h5ad" file used to save the AnnData object. If `None`,
    an in-memory AnnData object is returned.
prefix
    Any prefix before `matrix.mtx`, `genes.tsv` and `barcodes.tsv`. For instance,
    if the files are named `patientA_matrix.mtx`, `patientA_genes.tsv` and
    `patientA_barcodes.tsv`, then the prefix is `patientA_`.

Returns
-------
AnnData
    An AnnData object.
```

## snapatac2.read_dataset

Source module: `snapatac2._snapatac2`

Signature:

```python
snapatac2.read_dataset(filename, *, adata_files_update=None, mode='r+', backend=None)
```

Docstring:

```text
Read AnnDataSet object.

Read AnnDataSet from .h5ads file. If the file paths stored in AnnDataSet
object are relative paths, it will look for component .h5ad files in .h5ads file's parent directory.

Parameters
----------
filename: Path
    File name.
adata_files_update: Mapping[str, Path] | Path | None
    AnnDataSet internally stores links to component anndata files.
    You can find this information in `.uns['AnnDataSet']`.
    These links may be invalid if the anndata files are moved to a different location.
    This parameter provides a way to update the locations of component anndata files.
    The value of this parameter can be either a mapping from component anndata file names to their new locations,
    or a directory containing component anndata files.
mode: str
    "r": Read-only mode; "r+": can modify annotation file but not component anndata files.
backend: Literal['hdf5', 'zarr']
    Backend to use for reading the annotation file.

Returns
-------
AnnDataSet
```

## snapatac2.read_motifs

Source module: `snapatac2._snapatac2`

Signature:

```python
snapatac2.read_motifs(filename)
```

Docstring:

```text
Read motifs from a MEME format file.

Parameters
----------
filename: str | Path
    Path to the MEME format file.

Returns
-------
list[PyDNAMotif]
    List of `PyDNAMotif` objects.
```

## snapatac2.read_mtx

Source module: `snapatac2._snapatac2`

Signature:

```python
snapatac2.read_mtx(mtx_file, *, obs_names=None, var_names=None, file=None, backend=None, sorted=False)
```

Docstring:

```text
Read Matrix Market file.

Parameters
----------

mtx_file
    File name of the input matrix market file.
obs_names
    File that stores the observation names.
var_names
    File that stores the variable names.
file
    File name of the output ".h5ad" file.
backend: Literal['hdf5', 'zarr']
    Backend to use for writing the output file.
sorted
    If true, the input matrix is assumed to be sorted by rows.
    Sorted input matrix can be read faster.
```

## snapatac2.set_write_options

Source module: `snapatac2._snapatac2`

Signature:

```python
snapatac2.set_write_options(config)
```

Docstring:

```text
Set the default write configuration for all subsequent write operations.

This configuration is stored in thread-local storage and applies to all
dataset write operations that don't explicitly specify a configuration.

Parameters
----------
config : dict, optional
    Dictionary with optional keys:
    - "compression": Compression or None
    - "block_size": list of int or None

Examples
--------
>>> import anndata_rs
>>> # Set Gzip compression with custom block size
>>> anndata_rs.set_write_options({
...     "compression": anndata_rs.Compression.gzip(9),
...     "block_size": [1024, 1024],
... })
>>> # Set only compression
>>> anndata_rs.set_write_options({
...     "compression": anndata_rs.Compression.zstd(10)
... })
```
