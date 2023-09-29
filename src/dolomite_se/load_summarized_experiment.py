from typing import Any
from summarizedexperiment import SummarizedExperiment
from dolomite_base import load_object, acquire_metadata


def load_summarized_experiment(meta: dict[str, Any], project, **kwargs) -> SummarizedExperiment:
    """Load a 
    :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`
    from its on-disk representation. This method should generally not be 
    called directly but instead be invoked by 
    :py:meth:`~dolomite_base.load_object.load_object`.

    Args:
        meta: Metadata for this object.

        project: Value specifying the project of interest. This is most
            typically a string containing a file path to a staging directory
            but may also be an application-specific object that works with
            :py:meth:`~dolomite_base.acquire_file.acquire_file`.

        kwargs: Further arguments, ignored.

    Returns:
        A
        :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`
        with file-backed arrays in the assays.
    """
    se_meta = meta["summarized_experiment"]

    row_data = None 
    if "row_data" in se_meta:
        try:
            child_meta = acquire_metadata(project, se_meta["row_data"]["resource"]["path"])
            row_data = load_object(child_meta, project)
        except Exception as ex:
            raise ValueError("failed to load row data from '" + meta["$schema"] + "'; " + str(ex))

    col_data = None 
    if "column_data" in se_meta:
        try:
            child_meta = acquire_metadata(project, se_meta["column_data"]["resource"]["path"])
            col_data = load_object(child_meta, project)
        except Exception as ex:
            raise ValueError("failed to load column data from '" + meta["$schema"] + "'; " + str(ex))

    assays = {}
    for y in se_meta["assays"]:
        curname = y["name"]
        try:
            child_meta = acquire_metadata(project, y["resource"]["path"])
            assays[curname] = load_object(child_meta, project)
        except Exception as ex:
            raise ValueError("failed to load assay '" + curname + "' from '" + meta["$schema"] + "'; " + str(ex))

    return SummarizedExperiment(
        assays=assays,
        row_data=row_data,
        col_data=col_data
    )
