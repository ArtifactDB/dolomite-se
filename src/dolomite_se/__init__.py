import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "dolomite-se"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .read_summarized_experiment import read_summarized_experiment
from .save_summarized_experiment import save_summarized_experiment
from .save_ranged_summarized_experiment import save_ranged_summarized_experiment
from .read_ranged_summarized_experiment import read_ranged_summarized_experiment
from .utils import save_common_se_props, read_common_se_props