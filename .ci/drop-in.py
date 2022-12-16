print(f"Loading {__file__}")

from datetime import datetime
from ophyd.utils import make_dir_tree
from pprint import pprint

root_dir = "/tmp/basler"
_ = make_dir_tree(datetime.now().year, base_path=root_dir)

pprint(GT9V.read())
pprint(GT10V.read())
pprint(GQ10.read())
pprint(GQ11.read())
pprint(GQ12.read())
pprint(HeNe1.read())

pprint(fg3.read())

pprint(GPOP13.read())
pprint(GPOP13.summary())

# Basler + Laser scan:
uid1, = RE(bp.scan([GPOP13], HeNe1, 0, 5, 6))
hdr1 = db[uid1]
print(hdr1.table())
data = np.array(list(hdr1.data(field="GPOP13_cam_image", fill=True)))
print(f"{data.shape = }")

# MAD-X simulations (equivalent of "count" with default parameters):
uid2, = RE(bp.fly([madx_flyer]))
hdr2 = db[uid2]
print(hdr2.table(stream_name="madx_flyer", fill=True).T)

# MAD-X simulations (equivalent of "count" with changed parameter(s)):
def madx_plan():
    yield from bps.mv(fq1.k1, "ifq1/5.4444e-3/hr")
    yield from bp.fly([madx_flyer])

uid3, = RE(madx_plan())
hdr3 = db[uid3]
print(hdr3.table(stream_name="madx_flyer", fill=True).T)
