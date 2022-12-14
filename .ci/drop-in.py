print(GT9V.read())
print(GT10V.read())
print(GQ10.read())
print(GQ11.read())
print(GQ12.read())

print(fg3.read())

uid, = RE(bp.fly([madx_flyer]))

hdr = db[uid]
print(hdr.table(stream_name="madx_flyer", fill=True))

def madx_plan():
    yield from bps.mv(fq1.k1, "ifq1/5.4444e-3/hr")
    yield from bp.fly([madx_flyer])

uid2, = RE(madx_plan())

hdr2 = db[uid2]

print(hdr2.table(stream_name="madx_flyer", fill=True))
