print(f"Loading {__file__}")

from databroker.v0 import Broker
from bluesky import RunEngine
from bluesky.callbacks.best_effort import BestEffortCallback

import bluesky.plans as bp
import bluesky.plan_stubs as bps

import matplotlib.pyplot as plt

# Enable interactive mode
plt.ion()

# db = Broker.named("temp")
db = Broker.named("local")

RE = RunEngine({})
RE.subscribe(db.insert)

bec = BestEffortCallback()
RE.subscribe(bec)
