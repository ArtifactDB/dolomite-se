import os

import dolomite_base as dl
from _utils import _save_common_se_props
from summarizedexperiment import RangedSummarizedExperiment


@dl.save_object.register
@dl.validate_saves
def save_range_summarized_experiment(
    x: RangedSummarizedExperiment,
    path: str,
    data_frame_args: dict = None,
    assay_args: dict = None,
    **kwargs,
):
    """Method for saving
    :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`
    objects to their corresponding file representations, see
    :py:meth:`~dolomite_base.save_object.save_object` for details.

    Args:
        x:
            Object to be staged.

        path:
            Path to a directory in which to save ``x``.

        data_frame_args:
            Further arguments to pass to the ``save_object`` method for the
            row/column data.

        assay_args:
            Further arguments to pass to the ``save_object`` method for the
            assays.

        kwargs: Further arguments, ignored.

    Returns:
        Metadata that can be edited by calling methods and then saved with
        :py:meth:`~dolomite_base.write_metadata.write_metadata`.
    """
    os.mkdir(path)

    if data_frame_args is None:
        data_frame_args = {}

    if assay_args is None:
        assay_args = {}

    _se_meta = f"{list(x.shape)}"

    with open(os.path.join(path, "OBJECT"), "w", encoding="utf-8") as handle:
        handle.write(
            '{ "type": "range_summarized_experiment", "summarized_experiment": { "version": "1.0", "dimensions": '
            + _se_meta
            + " } }"
        )

    _save_common_se_props(
        x, path, data_frame_args=data_frame_args, assay_args=assay_args
    )

    _ranges = x.get_row_ranges()
    if _ranges is not None:
        dl.save_object(_ranges, path=os.path.join(path, "row_ranges"))

    return
