print(f"Loading {__file__}")

import os
import datetime

from sirepo_bluesky.sirepo_bluesky import SirepoBluesky
from sirepo_bluesky.sirepo_ophyd import create_classes
from sirepo_bluesky.madx_flyer import MADXFlyer
from sirepo_bluesky.madx_handler import MADXFileHandler

from ophyd.utils import make_dir_tree

db.reg.register_handler("madx", MADXFileHandler, overwrite=True)

root_dir = os.path.expanduser("~/sirepo_flyer_data")
_ = make_dir_tree(datetime.datetime.now().year, base_path=root_dir)

ATF_SIREPO_URL = os.getenv("ATF_SIREPO_URL")
if ATF_SIREPO_URL in (None, ""):
    print("ATF_SIREPO_URL environment variable should be set to use Sirepo.")
else:
    print(f"Using Sirepo at {ATF_SIREPO_URL}")
    connection = SirepoBluesky(ATF_SIREPO_URL)
    data, schema = connection.auth("madx", "00000002")

    classes, objects = create_classes(connection.data, connection=connection)
    globals().update(**objects)

    madx_flyer = MADXFlyer(
        connection=connection,
        root_dir=root_dir,
        report="elementAnimation250-20",
    )

# RE(bp.fly([madx_flyer]))
#
# hdr = db["2c8504e4-8ac9-4e56-ab42-da5e3cb9b4e0"]
# hdr.table(stream_name="madx_flyer", fill=True)
#
# def madx_plan():
#     yield from bps.mv(fq1.k1, "ifq1/5.4444e-3/hr")
#     yield from bp.fly([madx_flyer])
#
# RE(madx_plan())
#
# hdr2 = db["a3ed4aea-068e-4b15-85f7-3abdcf5cccc2"]
#
# hdr.table(stream_name="madx_flyer", fill=True).loc[21]
# hdr2.table(stream_name="madx_flyer", fill=True).loc[21]
