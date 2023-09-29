from typing import Any
from summarizedexperiment import SummarizedExperiment
from dolomite_base import stage_object, write_metadata
import dolomite_matrix # for the methods that are likely required by stage_object on the assays.
import os


@stage_object.register
def stage_summarized_experiment(
    x: SummarizedExperiment, 
    dir: str, 
    path: str, 
    is_child: bool = False, 
    data_frame_args: dict = {}, 
    assay_args: dict = {},
    **kwargs,
) -> dict[str, Any]:
    """Method for saving
    :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`
    objects to file, see
    :py:meth:`~dolomite_base.stage_object.stage_object` for details.

    Args:
        x: ``SummarizedExperiment`` to be saved.

        dir: Staging directory.

        path: Relative path inside ``dir`` to save the object.

        is_child: Is ``x`` a child of another object?

        data_frame_args: 
            Further arguemnts to pass to the ``stage_object`` method for the
            row/column data.

        assay_args: 
            Further arguemnts to pass to the ``stage_object`` method for the
            assays.

        kwargs: Further arguments, ignored.

    Returns:
        Metadata that can be edited by calling methods and then saved with 
        :py:meth:`~dolomite_base.write_metadata.write_metadata`.
    """
    os.makedirs(os.path.join(dir, path))
    se_meta = {
        "dimensions": list(x.shape)
    }

    assays = []
    for k, a in x.assays.items():
        newpath = path + "/assay-" + str(len(assays))
        try:
            ass_meta = stage_object(a, dir, newpath, is_child=True, **assay_args)
            ass_stub = write_metadata(ass_meta, dir)
        except Exception as ex:
            raise ValueError("failed to stage assay '" + k + "' for a " + str(type(x)) + "; " + str(ex))
        assays.append({ "name": k, "resource": ass_stub })
    se_meta["assays"] = assays

    if x.row_data.row_names is not None or x.row_data.shape[1] > 0:
        try:
            rd_meta = stage_object(x.row_data, dir, path + "/row_data", **data_frame_args)
            rd_stub = write_metadata(rd_meta, dir)
        except Exception as ex:
            raise ValueError("failed to stage row data for a " + str(type(x)) + "; " + str(ex))
        se_meta["row_data"] = { "resource": rd_stub }

    if x.col_data.row_names is not None or x.col_data.shape[1] > 0:
        try:
            cd_meta = stage_object(x.col_data, dir, path + "/column_data", **data_frame_args)
            cd_stub = write_metadata(cd_meta, dir)
        except Exception as ex:
            raise ValueError("failed to stage row data for a " + str(type(x)) + "; " + str(ex))
        se_meta["column_data"] = { "resource": cd_stub }

    return {
        "$schema": "summarized_experiment/v1.json",
        "path": path + "/experiment.json",
        "is_child": is_child,
        "summarized_experiment": se_meta,
    }
