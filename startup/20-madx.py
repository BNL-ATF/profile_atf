print(f"Loading {__file__}")

import os

ATF_SIREPO_URL = os.getenv("ATF_SIREPO_URL")
if ATF_SIREPO_URL in (None, ""):
    print("ATF_SIREPO_URL environment variable should be set to use Sirepo.")
else:
    import datetime

    from ophyd.utils import make_dir_tree
    from sirepo_bluesky.madx_flyer import MADXFlyer
    from sirepo_bluesky.madx_handler import MADXFileHandler
    from sirepo_bluesky.sirepo_bluesky import SirepoBluesky
    from sirepo_bluesky.sirepo_ophyd import create_classes

    db.reg.register_handler("madx", MADXFileHandler, overwrite=True)

    root_dir = os.path.expanduser("~/mnt/atfsim_sirepo/data/sirepo_flyer_data")
    _ = make_dir_tree(datetime.datetime.now().year, base_path=root_dir)

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


    def madx_plan(parameter="ihq1", value=2.0):
        """A bluesky plan to use MAD-X simulation package within Sirepo (via sirepo-bluesky lib).

        Run:

            uid, = RE(madx_plan())

        Data access:

            hdr = db[uid]
            tbl = hdr.table(stream_name="madx_flyer", fill=True)

        Plotting:

            plt.plot(tbl['madx_flyer_S'], tbl['madx_flyer_BETX'])
            plt.plot(tbl['madx_flyer_S'], tbl['madx_flyer_BETY'])

        """
        yield from bps.mv(objects_var[parameter].value, value)
        return (yield from bp.fly([madx_flyer]))
