<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/dolomite-se.svg?branch=main)](https://cirrus-ci.com/github/<USER>/dolomite-se)
[![ReadTheDocs](https://readthedocs.org/projects/dolomite-se/badge/?version=latest)](https://dolomite-se.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/dolomite-se/main.svg)](https://coveralls.io/r/<USER>/dolomite-se)
[![PyPI-Server](https://img.shields.io/pypi/v/dolomite-se.svg)](https://pypi.org/project/dolomite-se/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/dolomite-se.svg)](https://anaconda.org/conda-forge/dolomite-se)
[![Monthly Downloads](https://pepy.tech/badge/dolomite-se/month)](https://pepy.tech/project/dolomite-se)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/dolomite-se)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# Save and load SummarizedExperiments in Python

## Introduction

The **dolomite-se** package is the Python counterpart to the [**alabaster.se**](https://github.com/ArtifactDB/alabaster.se) R package,
providing methods for saving/reading `SummarizedExperiment` objects within the [**dolomite** framework](https://github.com/ArtifactDB/dolomite-base).
All components of the `SummarizedExperiment` - assays, row data and column data - are saved to their respective file representations,
which can be loaded in a new R/Python environment for cross-language analyses.

## Quick start

Let's mock up a `SummarizedExperiment`:

```python
import summarizedexperiment
import biocframe
import numpy

se = summarizedexperiment.SummarizedExperiment(
    assays={ "counts": numpy.random.rand(1000, 200) },
    row_data=biocframe.BiocFrame(
        { "foo": numpy.random.rand(1000) }, 
        row_names = ["gene" + str(i) for i in range(1000)]
    ),
    col_data=biocframe.BiocFrame(
        { "whee": numpy.random.rand(200) },
        row_names = ["cell" + str(i) for i in range(200)]
    )
)
```

Now we can save it:

```python
from dolomite_base import stage_object, write_metadata
import dolomite_se

dir = "test"
meta = stage_object(se, dir, "mydata")
write_metadata(meta, dir)
print(meta["path"])
## mydata/experiment.json
```

And load it again, e,g., in a new session:

```python
from dolomite_base import acquire_metadata, load_object

meta = acquire_metadata("test", "mydata/experiment.json")
reloaded = load_object(meta, dir)
## Class SummarizedExperiment with 1000 features and 200 samples
##   assays: ['counts']
##   row_data: ['foo']
##   col_data: ['whee']
```
