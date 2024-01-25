import os

import dolomite_base as dl
from dolomite_base.read_object import registry
from summarizedexperiment import SummarizedExperiment

from .read_summarized_experiment import read_summarized_experiment

registry["range_summarized_experiment"] = "dolomite_se.read_summarized_experiment"


def read_range_summarized_experiment(
    path: str, metadata: dict, **kwargs
) -> SummarizedExperiment:
    """Load a
    :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`
    from its on-disk representation.

    This method should generally not be called directly but instead be invoked by
    :py:meth:`~dolomite_base.read_object.read_object`.

    Args:
        path:
            Path to the directory containing the object.

        metadata:
            Metadata for the object.

        kwargs:
            Further arguments, ignored.

    Returns:
        A
        :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`
        with file-backed arrays in the assays.
    """

    rse = read_summarized_experiment(path, metadata, kwargs)

    _ranges_path = os.path.join(path, "row_ranges")
    if os.path.exists(_ranges_path):
        _ranges = dl.read_object(_ranges_path)
        rse = rse.set_row_ranges(_ranges)

    return rse
