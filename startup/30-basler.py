print(f"Loading {__file__}")

import numpy as np
import ophyd_basler
from ophyd_basler.basler_camera import BaslerCamera
from ophyd_basler.basler_handler import BaslerCamHDF5Handler

db.reg.register_handler("BASLER_CAM_HDF5", BaslerCamHDF5Handler, overwrite=True)

basler_device_metadata, basler_devices = ophyd_basler.available_devices()
print(basler_device_metadata)

GPOP13 = BaslerCamera(cam_num=4, verbose=True, pixel_format="Mono12", name="GPOP13")
