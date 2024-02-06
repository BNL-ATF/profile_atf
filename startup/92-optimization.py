import bloptools
from bloptools.bayesian import DOF, Objective, Agent

dofs = [
    DOF(device=LS1, search_bounds=(101, 103), units="A", active=False),
    DOF(device=HQ1, search_bounds=(7, 9), units="A"),
    DOF(device=HQ2, search_bounds=(-8, -6), units="A"),
    DOF(device=HQ3, search_bounds=(7, 9), units="A"),
]

objectives = [
    Objective(description="flux", name="fg3_sum_pixels", log=True, max_noise=1e-1),
    Objective(description="horizontal spread", name="fg3_xsig", target="min", log=True, max_noise=1e-1),
    Objective(description="vertical spread", name="fg3_ysig", target="min", log=True, max_noise=1e-1),
    Objective(description="shape ratio", name="log_shape_ratio", target="min", log=False, max_noise=1e-1),
]

dets = [fg3]

def digestion(db, uid):

    products = db[uid].table(fill=True)

    for index, entry in products.iterrows():

        products.loc[index, "flux_density"] = entry.fg3_sum_pixels / (entry.fg3_xsig ** 2 + entry.fg3_ysig ** 2)
        products.loc[index, "log_shape_ratio"] = np.abs(np.log(entry.fg3_xsig / entry.fg3_ysig))

    return products

agent = Agent(dofs=dofs,
              objectives=objectives,
              dets=dets,
              db=db,
              digestion=digestion,
              verbose=True,
              trigger_delay=0.7)
