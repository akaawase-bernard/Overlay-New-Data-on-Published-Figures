



import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Speed axis (log-spaced)
# -------------------------
c = np.linspace(0.2, 10, 250)   # ~0.06 to 10 m/s

# -------------------------
# Shape parameters
# -------------------------
A  = 0.6
cp = 0.6
ct = 1.2
p  = 1.4
q  = 2.2

# -------------------------
# Core spectrum
# -------------------------
S = (
    A
    * (c / cp) ** p
    * np.exp(-(c / cp) ** q)
    * (1 + (c / ct) ** 6) ** -1
)

# -------------------------
# Add noise
# -------------------------
noise_level = 0.08
S *= np.exp(noise_level * np.random.randn(len(S)))

# -------------------------
# Save CSV (NO HEADER)
# -------------------------
np.savetxt(
    "data/new_dataset.csv",
    np.column_stack([c, S]),
    delimiter=","
)

# -------------------------
# Sanity-check plot
# -------------------------
plt.loglog(c, S, lw=3)
#plt.ylim(1e-6, 1e-3)

plt.loglog(c, c**-6, "k--", lw=2, label=r"$c^{-6}$")
plt.xlabel(r"$c$ (m/s)")
plt.ylabel(r"$S(c)$")
plt.legend()
plt.grid(True, which="both", ls=":")
plt.show()
