print(f"Loading {__file__}")

import logging
import os

import numpy as np
import ophyd_basler
from ophyd_basler.basler_camera import BaslerCamera
from ophyd_basler.basler_handler import BaslerCamHDF5Handler
from ophyd_basler.utils import configure_logger, logger_basler

configure_logger(logger_basler, logging.INFO)

db.reg.register_handler("BASLER_CAM_HDF5", BaslerCamHDF5Handler, overwrite=True)

basler_device_metadata, basler_devices = ophyd_basler.available_devices()
print(basler_device_metadata)

# Add an option to override the value via environment variables (useful for CI).
# The "Mono12" mode is not available for the emulated cameras.
pixel_format = os.getenv("PYLON_CAM_PIXEL_FORMAT", "Mono12")

GPOP13 = BaslerCamera(
    cam_num=4,
    verbose=True,
    pixel_format=pixel_format,
    name="GPOP13",
    root_dir=os.path.expanduser("~/mnt/atfsim_sirepo/data/basler"),
)
