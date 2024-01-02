import sys

import numpy as np
import matplotlib.pyplot as plt
import json

#Read data used in the simulation
with open(sys.argv[1], "r") as f:
    param = json.load(f)

with open(sys.argv[2], "r") as f:
    result = json.load(f)

time = result["graphics"]["x0"]
impedanceReal = result["graphics"]["y0"]
impedanceImag = result["graphics"]["y1"]

radius    = param["rParticle"]
vwallL    = param["vwall"]
vwall     = complex(vwallL[0], vwallL[1])

Lxy    = param["Lxy"]
theta = np.pi*radius**2/Lxy**2
plt.plot(time, np.array(impedanceReal)/theta, ".-", color = "red", label = "$Re(Z_{iter})$")
plt.plot(time, np.array(impedanceImag)/theta, ".-", color = "blue", label = "$Im(Z_{iter})$")

plt.xlabel("Iteration")
plt.ylabel("$Z/Z_{fluid}$")
plt.legend(fontsize = 20, loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()
