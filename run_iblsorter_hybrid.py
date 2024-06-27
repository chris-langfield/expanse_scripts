import shutil
from pathlib import Path
import sys

import iblsorter
from iblsorter.ibl import run_spike_sorting_ibl, ibl_pykilosort_params

from viz import reports


pid = sys.argv[1]
print(pid)

hybrid_path = Path("/expanse/lustre/projects/col168/clangfield/data/re_hybrid/")
bin_file = hybrid_path.joinpath(pid, "recording", "traces_cached_seg0.raw")

params = ibl_pykilosort_params(bin_file)
print(params)