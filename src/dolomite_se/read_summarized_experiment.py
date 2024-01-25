import json
import os

import dolomite_base as dl
import dolomite_matrix as dlm
from dolomite_base.read_object import registry
from summarizedexperiment import SummarizedExperiment

registry["summarized_experiment"] = "dolomite_se.read_summarized_experiment"


def read_summarized_experiment(
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

    _row_data = None
    _rdata_path = os.path.join(path, "row_data")
    if os.path.exists(_rdata_path):
        _row_data = dl.read_object(_rdata_path)

    _column_data = None
    _cdata_path = os.path.join(path, "column_data")
    if os.path.exists(_cdata_path):
        _column_data = dl.read_object(_cdata_path)

    _assays_path = os.path.join(path, "assays")
    with open(os.path.join(_assays_path, "names.json"), "r") as handle:
        _assay_names = json.load(handle)

    _assays = {}
    for _aidx, _aname in enumerate(_assay_names):
        _assay_read_path = os.path.join(_assays_path, str(_aidx))

        try:
            _assays[_aname] = dl.read_object(_assay_read_path)
        except Exception as ex:
            raise RuntimeError(
                f"failed to load assay '{_aname}' from '{path}'; " + str(ex)
            )

    se = SummarizedExperiment(
        assays=_assays, row_data=_row_data, column_data=_column_data
    )

    _meta_path = os.path.join(path, "other_data")
    if os.path.exists(_meta_path):
        _meta = dl.read_object(_meta_path)
        se = se.set_metadata(_meta.as_dict())

    return se
