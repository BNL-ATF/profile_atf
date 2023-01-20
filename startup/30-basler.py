print(f"Loading {__file__}")

import os
import numpy as np
import ophyd_basler
from ophyd_basler.basler_camera import BaslerCamera
from ophyd_basler.basler_handler import BaslerCamHDF5Handler

###############################################################################
import logging
from logging import StreamHandler

logger = logging.getLogger("basler")
stream_handler = StreamHandler()
log_file_format = (
    "[%(levelname)1.1s %(asctime)s.%(msecs)03d %(name)s"
    "  %(module)s:%(lineno)d] %(message)s"
)
stream_handler.setFormatter(logging.Formatter(fmt=log_file_format))
logger.addHandler(stream_handler)

# logger.setLevel(logging.DEBUG)
# stream_handler.setLevel(logging.DEBUG)

logger.setLevel(logging.INFO)
stream_handler.setLevel(logging.INFO)
###############################################################################

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
    root_dir=os.path.expanduser("~/basler"),
)
