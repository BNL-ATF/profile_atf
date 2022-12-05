import datetime
import itertools

import matplotlib.pyplot as plt
import numpy as np
from pypylon import pylon

from ophyd import Component as Cpt
from ophyd import Device, Signal
from ophyd.sim import NullStatus

import os

os.environ['PYLON_CAMEMU'] = "1"

plt.ion()

class BaslerCamera(Device):

    image = Cpt(Signal, kind="normal")
    mean  = Cpt(Signal, kind="hinted")
    shape = Cpt(Signal, kind="normal")

    def __init__(self, name='basler_cam',
                    sim_id=None, watch_name=None,
                    sirepo_server='http://10.10.10.10:8000', source_simulation=False,
                    root_dir='/tmp/sirepo_det_data', **kwargs):
        super().__init__(name=name, **kwargs)

        transport_layer_factory = pylon.TlFactory.GetInstance()
        device_info_list = transport_layer_factory.EnumerateDevices()
        print(device_info_list)

        number_of_devices = len(device_info_list)
        print(f"{number_of_devices = }")

        self.device_info = device_info_list[0]
        self.device = transport_layer_factory.CreateDevice(self.device_info)
        self.camera_object = pylon.InstantCamera(self.device)

        self.camera_object.Open()

        self.user_defined_name = self.camera_object.GetDeviceInfo().GetUserDefinedName()
        self.camera_model = self.camera_object.GetDeviceInfo().GetModelName()
        self.camera_serial_no = self.camera_object.GetDeviceInfo().GetSerialNumber()
        self.width = self.camera_object.Width()
        self.height = self.camera_object.Height()
        self.pixel_level_min = self.camera_object.PixelDynamicRangeMin()
        self.pixel_level_max = self.camera_object.PixelDynamicRangeMax()
        self.active_format = self.camera_object.PixelFormat.GetValue()
        self.formats_supported = self.camera_object.PixelFormat.Symbolics
        self.payload_size = self.camera_object.PayloadSize()
        self.grab_timeout = 5000 # ms

        self.camera_object.Close()

    def grab_images(self, num=10):

        self.camera_object.StartGrabbingMax(num)
        counter = itertools.count()
        first_image = np.zeros((self.height, self.width))
        while self.camera_object.IsGrabbing():
            grab_result = self.camera_object.RetrieveResult(self.grab_timeout, pylon.TimeoutHandling_ThrowException)
            if grab_result.GrabSucceeded():
                image = grab_result.Array
                current_frame = next(counter)
                if current_frame == 1:
                    first_image = np.copy(image)
                print(
                    f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} "
                    f"{current_frame:04d} {image.shape = } {image.mean() = } "
                    f"{image[0, 0] = } {image[-1, -1] = }"
                )

            grab_result.Release()

        self.camera_object.StopGrabbing()

        return image

    def trigger(self, verbose=True):

        super().trigger()

        self.camera_object.Open()

        trigger_mode = "Off"

        if verbose:
            print("User-defined camera name    :", self.user_defined_name)
            print("Camera model                :", self.camera_model)
            print("Camera serial number        :", self.camera_serial_no)
            print("Image width  (X, ncols)     :", self.width, "pixels")
            print("Image height (Y, nrows)     :", self.height, "pixels")
            print("Pixel format                :", self.active_format)
            print("Camera min. pixel level     :", self.pixel_level_min)
            print("Camera max. pixel level     :", self.pixel_level_max)
            print("Grab timeout                :", self.grab_timeout, "ms")
            print("Trigger mode                :", trigger_mode)
            print("GigE transport payload size : " + "{:,}".format(self.payload_size) + " bytes")
            print("\nCamera supported pixel formats:\n", self.formats_supported)

        self.camera_object.TriggerMode.SetValue(trigger_mode)
        desired_pixel_format = "Mono8"
        self.camera_object.PixelFormat.SetValue(desired_pixel_format)

        image = self.grab_images(num=10)
        self.update_components(image)
        self.camera_object.Close()

    def update_components(self, image):

        self.image.put(image)
        self.shape.put(image.shape)
        self.mean.put(image.mean())

cam = BaslerCamera()
cam.trigger()
