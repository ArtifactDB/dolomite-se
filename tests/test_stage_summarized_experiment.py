import dolomite_se
from dolomite_base import stage_object, write_metadata, load_object
import summarizedexperiment
import filebackedarray
import biocframe
import numpy
from tempfile import mkdtemp
import os


def test_stage_summarized_experiment_simple():
    x = numpy.random.rand(1000, 200)
    se = summarizedexperiment.SummarizedExperiment({ "counts": x })

    dir = mkdtemp()
    info = stage_object(se, dir, "se")
    assert "row_data" not in info["summarized_experiment"]
    assert "column_data" not in info["summarized_experiment"]
    write_metadata(info, dir)

    roundtrip = load_object(info, dir)
    assert isinstance(roundtrip, summarizedexperiment.SummarizedExperiment)
    ass = roundtrip.assay("counts")
    assert isinstance(ass, filebackedarray.Hdf5DenseArray)

    # Works with multiple assays.
    x2 = (numpy.random.rand(1000, 200) * 10).astype(numpy.int32)
    se = summarizedexperiment.SummarizedExperiment({ "logcounts": x, "counts": x2 })

    dir = mkdtemp()
    info = stage_object(se, dir, "se")
    write_metadata(info, dir)

    roundtrip = load_object(info, dir)
    assert roundtrip.assay_names == [ "logcounts", "counts" ]


def test_stage_summarized_experiment_with_dimdata():
    x = numpy.random.rand(1000, 200)
    se = summarizedexperiment.SummarizedExperiment(
        assays={ "counts": x },
        row_data=biocframe.BiocFrame({ "foo": numpy.random.rand(1000), "bar": numpy.random.rand(1000) }),
        col_data=biocframe.BiocFrame({ "whee": numpy.random.rand(200), "stuff": numpy.random.rand(200) }),
    )

    dir = mkdtemp()
    info = stage_object(se, dir, "se")
    assert "row_data" in info["summarized_experiment"]
    assert "column_data" in info["summarized_experiment"]
    write_metadata(info, dir)

    roundtrip = load_object(info, dir)
    assert isinstance(roundtrip, summarizedexperiment.SummarizedExperiment)
    assert numpy.allclose(se.row_data["foo"], roundtrip.row_data["foo"])
    assert numpy.allclose(se.col_data["stuff"], roundtrip.col_data["stuff"])

    # What about just row names.
    se = summarizedexperiment.SummarizedExperiment(
        assays={ "counts": x },
        row_data=biocframe.BiocFrame(row_names = ["gene" + str(i) for i in range(1000)]),
        col_data=biocframe.BiocFrame(row_names = ["cell" + str(i) for i in range(200)])
    )

    dir = mkdtemp()
    info = stage_object(se, dir, "se")
    assert "row_data" in info["summarized_experiment"]
    assert "column_data" in info["summarized_experiment"]
    write_metadata(info, dir)

    roundtrip = load_object(info, dir)
    assert isinstance(roundtrip, summarizedexperiment.SummarizedExperiment)
    assert se.row_data.row_names == roundtrip.row_data.row_names
    assert se.col_data.row_names == roundtrip.col_data.row_names
