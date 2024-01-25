import os
from tempfile import mkdtemp

import biocframe
import dolomite_se
import filebackedarray
import numpy
import summarizedexperiment
from dolomite_base import read_object, save_object


def test_stage_se_simple():
    x = numpy.random.rand(1000, 200)
    se = summarizedexperiment.SummarizedExperiment({"counts": x})

    dir = os.path.join(mkdtemp(), "se_simple")
    save_object(se, dir)

    roundtrip = read_object(dir)
    assert isinstance(roundtrip, summarizedexperiment.SummarizedExperiment)
    ass = roundtrip.assay("counts")
    assert isinstance(ass, filebackedarray.Hdf5DenseArray)

    # Works with multiple assays.
    x2 = (numpy.random.rand(1000, 200) * 10).astype(numpy.int32)
    se = summarizedexperiment.SummarizedExperiment({"logcounts": x, "counts": x2})

    dir = os.path.join(mkdtemp(), "se_simple2")
    save_object(se, dir)

    roundtrip = read_object(dir)
    assert roundtrip.assay_names == ["logcounts", "counts"]


def test_stage_se_with_dimdata():
    x = numpy.random.rand(1000, 200)
    se = summarizedexperiment.SummarizedExperiment(
        assays={"counts": x},
        row_data=biocframe.BiocFrame(
            {"foo": numpy.random.rand(1000), "bar": numpy.random.rand(1000)}
        ),
        column_data=biocframe.BiocFrame(
            {"whee": numpy.random.rand(200), "stuff": numpy.random.rand(200)}
        ),
    )

    dir = os.path.join(mkdtemp(), "se_dimdata")
    save_object(se, dir)

    roundtrip = read_object(dir)
    assert isinstance(roundtrip, summarizedexperiment.SummarizedExperiment)
    assert numpy.allclose(se.row_data["foo"], roundtrip.row_data["foo"])
    assert numpy.allclose(se.column_data["stuff"], roundtrip.column_data["stuff"])

    # What about just row names.
    se = summarizedexperiment.SummarizedExperiment(
        assays={"counts": x},
        row_data=biocframe.BiocFrame(row_names=["gene" + str(i) for i in range(1000)]),
        column_data=biocframe.BiocFrame(row_names=["cell" + str(i) for i in range(200)]),
    )

    dir = os.path.join(mkdtemp(), "se_dimdata2")
    save_object(se, dir)

    roundtrip = read_object(dir)
    assert isinstance(roundtrip, summarizedexperiment.SummarizedExperiment)
    assert se.row_data.row_names == roundtrip.row_data.row_names
    assert se.column_data.row_names == roundtrip.col_data.row_names


def test_stage_se_with_other_meta():
    x = numpy.random.rand(1000, 200)
    se = summarizedexperiment.SummarizedExperiment(
        assays={"counts": x}, metadata={"YAY": 2, "FOO": "a"}
    )

    dir = os.path.join(mkdtemp(), "se_other_meta")
    save_object(se, dir)

    roundtrip = read_object(dir)
    assert roundtrip.metadata == se.metadata
