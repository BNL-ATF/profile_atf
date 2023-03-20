print(f"Loading {__file__}")

import os
import time as ttime
from contextlib import ContextDecorator

from atfdb import atfdb
from atfdb.ophyd import ATFSignalNoConn, ReadOnlyException, open_close_conn
from ophyd import Component as Cpt
from ophyd import Device, Signal
from ophyd.sim import NullStatus

ATF_SOCKET_HOST = os.getenv("ATF_SOCKET_HOST")
if ATF_SOCKET_HOST is None:
    raise RuntimeError("ATF_SOCKET_HOST environment variable should be set.")

ATF_SOCKET_PORT = int(os.getenv("ATF_SOCKET_PORT"))


def check_conn_once(envvar="ATF_OPEN_CONN_ONCE"):
    import os

    connect_once = os.getenv(envvar)
    if connect_once is not None and connect_once.lower() in ["y", "yes", "1", "true"]:
        return True
    else:
        return False


if check_conn_once():
    print("Opening socket connection to atf_db...")
    atfdb.host_connect(ATF_SOCKET_HOST, ATF_SOCKET_PORT)  # generate socket

PS_H_line = {
    "LT1HX": "CAEN3",
    "LT1VX": "CAEN2",
    "LT2HX": "CAEN1",
    "LT2VX": "CAEN4",
    "LS1": "PTEN17",
    "TK1H": "CAEN13",
    "TK1V": "CAEN14",
    "TK2H": "CAEN15",
    "TK2V": "CAEN16",
    "TK3H": "CAEN17",
    "TK3V": "CAEN18",
    "HT1H": "DARL1",
    "HT1V": "DARL2",
    "HT2H": "DARL3",
    "HT2V": "DARL4",
    "HQ1": "DARL149",
    "HQ2": "DARL150",
    "HQ3": "DARL151",
    "HT3H": "DARL9",
    "HT3V": "DARL10",
    "HT4H": "DARL27",
    "HT4V": "DARL28",
    "HQ4": "DARL152",
    "HQ5": "DARL153",
    "HQ6": "DARL154",
    "HT5H": "DARL29",
    "HT5V": "DARL30",
    "HT6H": "DARL31",
    "HT6V": "DARL32",
    "HQ7": "DARL155",
    "HQ8": "DARL156",
    "HQ9": "DARL157",
    "HD1X": "CAEN5",
    "FT1H": "DARL5",
    "FT1V": "DARL6",
    "FQ1": "DARL137",
    "FQ2": "DARL138",
    "FQ3": "DARL139",
    "FT2H": "DARL7",
    "FT2V": "DARL8",
    "GD1X": "CAEN6",
    "GQ1": "DARL169",
    "GQ2": "DARL170",
    "GQ3": "DARL171",
    "GT1H": "DARL11",
    "GT1V": "DARL12",
    "GT2H": "DARL19",
    "GT2V": "DARL20",
    "GQ4": "DARL172",
    "GQ5": "DARL173",
    "GQ6": "DARL174",
    "GT3H": "DARL21",
    "GT3V": "DARL22",
    "GT5H": "DARL33",
    "GT5V": "DARL34",
    "GQ7": "DARL178",
    "GQ8": "DARL179",
    "GQ9": "DARL190",
    "GT7H": "DARL69",
    "GT7V": "DARL70",
    "GT8H": "DARL71",
    "GT8V": "DARL72",
    "GQ10": "DARL191",  # Use on 2022-09-02
    "GQ11": "DARL175",  # ...
    "GQ12": "DARL176",  # ...
    "GT9H": "DARL65",
    "GT9V": "DARL66",
    "GT10H": "DARL35",
    "GT10V": "DARL36",
    "GD3": "PTEN04",
    "HeNe1": "PTEN20",  # alignment laser
}

channel_dict = {}
for tag, name in PS_H_line.items():
    channel_dict[tag] = {}
    channel_dict[tag]["name"] = name
    if name[:4] == "CAEN":
        channel_dict[tag]["db"] = "CAEN_DB"
    else:
        channel_dict[tag]["db"] = "RT_DATABASE"

    if name[:4] == "PTEN":
        channel_dict[tag]["tol"] = 1e1
    if name[:4] == "DARL":
        channel_dict[tag]["tol"] = 1e-1
    if name[:4] == "CAEN":
        channel_dict[tag]["tol"] = 5e-3


class ATFSignalWithConn(ATFSignalNoConn):
    ...


for method in ("get", "get_setpoint", "_update_readback_setpoint", "put", "set"):
    setattr(
        ATFSignalWithConn,
        method,
        open_close_conn(socket_server=ATF_SOCKET_HOST, socket_port=ATF_SOCKET_PORT)(
            getattr(ATFSignalWithConn, method)
        ),
    )

if check_conn_once():
    ATFSignal = ATFSignalNoConn
else:
    ATFSignal = ATFSignalWithConn


class ATFSignalRO(ATFSignal):
    def put(self, *args, **kwargs):
        raise ReadOnlyException("Cannot set/put the read-only signal.")


class FrameGrabber(Device):
    db = "FRAME3_DB"
    psname = "FGR3"
    xpos = Cpt(
        ATFSignalRO,
        db=db,
        psname=psname,
        read_suffix="RCX;CENTROID_X",
        write_suffix="RCX;CENTROID_X",
        kind="hinted",
    )
    ypos = Cpt(
        ATFSignalRO,
        db=db,
        psname=psname,
        read_suffix="RCY;CENTROID_Y",
        write_suffix="RCY;CENTROID_Y",
        kind="hinted",
    )
    xsig = Cpt(
        ATFSignalRO,
        db=db,
        psname=psname,
        read_suffix="RSX;SIGMA_X",
        write_suffix="RSX;SIGMA_X",
        kind="hinted",
    )
    ysig = Cpt(
        ATFSignalRO,
        db=db,
        psname=psname,
        read_suffix="RSY;SIGMA_Y",
        write_suffix="RSY;SIGMA_Y",
        kind="hinted",
    )
    sum_pixels = Cpt(
        ATFSignalRO,
        db=db,
        psname=psname,
        read_suffix="RM00;SUM_PIXELS",
        write_suffix="RM00;SUM_PIXELS",
        dtype="double",
        kind="hinted",
    )


fg3 = FrameGrabber(name="fg3")


for el_id in ["TK1H", "GT9V", "GT10V", "GQ10", "GQ11", "GQ12", "HeNe1"]:
    el = channel_dict[el_id]
    channel_dict[el_id]["ophyd"] = ATFSignal(
        name=f"{el_id}_{el['name']}",  # ophyd API
        db=el["db"],
        psname=el["name"],
        tol=el["tol"],
        timeout=3.0 if el_id == "TK1H" else 2.0,
    )

TK1H = channel_dict["TK1H"]["ophyd"]
GT9V = channel_dict["GT9V"]["ophyd"]
GT10V = channel_dict["GT10V"]["ophyd"]
GQ10 = channel_dict["GQ10"]["ophyd"]
GQ11 = channel_dict["GQ11"]["ophyd"]
GQ12 = channel_dict["GQ12"]["ophyd"]
HeNe1 = channel_dict["HeNe1"]["ophyd"]
