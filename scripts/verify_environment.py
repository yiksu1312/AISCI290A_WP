"""Verify imports, versions, and a real Jupyter kernel execution."""
import importlib
import json
import sys
from jupyter_client import KernelManager

modules = ["numpy", "pandas", "matplotlib", "seaborn", "sklearn", "xarray",
           "dask", "netCDF4", "ipykernel", "jupyterlab", "nbconvert"]
versions = {name: importlib.import_module(name).__version__ for name in modules}
km = KernelManager(kernel_name="aisci290a")
km.start_kernel()
client = km.client()
client.start_channels()
try:
    client.wait_for_ready(timeout=60)
    reply = client.execute_interactive(
        "import sys, xarray, netCDF4; print(sys.executable)", timeout=60)
    if reply["content"]["status"] != "ok":
        raise RuntimeError(reply["content"])
finally:
    client.stop_channels()
    km.shutdown_kernel(now=True)
print(json.dumps({"python": sys.version, "executable": sys.executable,
                  "packages": versions, "kernel_execution": "passed"}, indent=2))
