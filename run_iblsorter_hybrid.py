import shutil
from pathlib import Path
import sys
import os


import numpy as np

import iblsorter
from iblsorter.ibl import run_spike_sorting_ibl
from iblsorter.params import KilosortParams
from iblsorter.utils import Bunch
from iblsorter.main import run

import spikeglx
import neuropixel

from viz import reports

pid = sys.argv[1]
print(pid)

hybrid_path = Path("/expanse/lustre/projects/col168/clangfield/data/re_hybrid/")
bin_file = hybrid_path.joinpath(pid, "recording", "traces_cached_seg0.raw")

dtype = np.float16
dsize = np.array([0]).astype(dtype).itemsize
nc = 384
fs = 30_000
filesize = os.stat(bin_file).st_size
ns = filesize / (dsize * nc)
assert ns.is_integer()
ns = int(ns)
print("Recording length: ", ns/fs, "sec")
print(ns, "samples")

sr = spikeglx.Reader(bin_file, ns=ns, dtype=dtype)

h = neuropixel.trace_header(version=1)
nc = h['x'].size
params = KilosortParams()
params.probe = iblsorter.io.probes.np1_probe()
params.probe["NchanTOT"] = nc
params.probe["sample2volt"] = sr.sample2volts[0]
params.minFR = 0
params.minfr_goodchannels = 0
params.probe.ind = h["ind"]
params.probe.row = h["row"]
params.probe.col = h["col"]
params.probe.x = h['x']
params.probe.y = h['y']
params.probe.shank = h['shank']
params.probe.channels_labels = np.zeros(nc, dtype=int)
params.probe.sample_shift = h['sample_shift']
params.probe.adc = h["adc"]
params.probe.h, params.probe.neuropixel_version = (h, 1)

params = dict(params)
params["data_dtype"] = "float16"

ephys_reader_args = {"dtype":dtype,
                     "sample_rate": sr.fs,
                     "n_channels": 384}
params["ephys_reader_args"] = ephys_reader_args
params = Bunch(params)

output_dir = hybrid_path.joinpath(pid, "pykilosort")
output_dir.mkdir(parents=True, exist_ok=True)
scratch_dir = Path("/tmp/pyks").joinpath(pid)
shutil.rmtree(scratch_dir, ignore_errors=True)
scratch_dir.mkdir(exist_ok=True, parents=True)

run(str(bin_file), dir_path=str(scratch_dir), output_dir=str(output_dir), **params)


