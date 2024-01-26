import json
import os

import dolomite_base as dl


def _save_common_se_props(x, path, data_frame_args, assay_args):
    # save assays
    _assays_path = os.path.join(path, "assays")
    os.mkdir(_assays_path)

    _assay_names = x.get_assay_names()
    with open(os.path.join(_assays_path, "names.json"), "w") as handle:
        json.dump(_assay_names, handle)

    for _aidx, _aname in enumerate(_assay_names):
        _assay_save_path = os.path.join(_assays_path, str(_aidx))
        try:
            dl.save_object(x.assays[_aname], path=_assay_save_path, **assay_args)
        except Exception as ex:
            raise RuntimeError(
                "failed to stage assay '"
                + _aname
                + "' for "
                + str(type(x))
                + "; "
                + str(ex)
            )

    # save row data
    _rdata = x.get_row_data()
    if _rdata is not None and (_rdata.row_names is not None or _rdata.shape[1] > 0):
        dl.save_object(_rdata, path=os.path.join(path, "row_data"), **data_frame_args)

    # save column data
    _cdata = x.get_column_data()
    if _cdata is not None and (_cdata.row_names is not None or _cdata.shape[1] > 0):
        dl.save_object(
            _cdata, path=os.path.join(path, "column_data"), **data_frame_args
        )

    _meta = x.get_metadata()
    if _meta is not None and len(_meta) > 0:
        dl.save_object(_meta, path=os.path.join(path, "other_data"))


def _read_common_se_props(path):
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

    return _row_data, _column_data, _assays
