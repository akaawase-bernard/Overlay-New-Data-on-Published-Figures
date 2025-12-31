import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from dataclasses import dataclass

# =========================
# Axis specification
# =========================
@dataclass
class AxisSpec:
    xscale: str = "linear"   # "linear" or "log"
    yscale: str = "linear"   # "linear" or "log"


# =========================
# Helpers
# =========================
def _transform(values, scale):
    values = np.asarray(values, dtype=float)
    if scale == "log":
        if np.any(values <= 0):
            raise ValueError("Log scale selected but values contain <= 0.")
        return np.log10(values)
    return values


def click_points(img, n, title):
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.imshow(img)
    ax.set_title(title)
    ax.axis("off")
    pts = plt.ginput(n, timeout=0)
    plt.close(fig)
    return np.array(pts)


def fit_axis_mapping(pixel_pts, data_pts, axis_spec):
    pixel_pts = np.asarray(pixel_pts)
    data_pts  = np.asarray(data_pts)

    u = pixel_pts[:, 0]
    v = pixel_pts[:, 1]

    x = _transform(data_pts[:, 0], axis_spec.xscale)
    y = _transform(data_pts[:, 1], axis_spec.yscale)

    A_x = np.c_[x, np.ones_like(x)]
    ax_, bx_ = np.linalg.lstsq(A_x, u, rcond=None)[0]

    A_y = np.c_[y, np.ones_like(y)]
    ay_, by_ = np.linalg.lstsq(A_y, v, rcond=None)[0]

    return (ax_, bx_), (ay_, by_)


def data_to_pixel(x, y, xfit, yfit, axis_spec):
    x = _transform(x, axis_spec.xscale)
    y = _transform(y, axis_spec.yscale)
    u = xfit[0] * x + xfit[1]
    v = yfit[0] * y + yfit[1]
    return u, v


# =========================
# MAIN FUNCTION (MODIFIED)
# =========================
def overlay_on_screenshot(
    screenshot_path,
    x_new,
    y_new,
    axis_spec,
    out_path,
    mode="line",
    linewidth=3.0,
    markersize=20,
):

    img = mpimg.imread(screenshot_path)

    # -------------------------
    # 1. Select plot box (visual sanity only)
    # -------------------------
    _ = click_points(
        img, 4,
        "Click plot box corners (for reference only)"
    )

    # -------------------------
    # 2. Calibration points
    # -------------------------
    calib_pixels = click_points(
        img, 4,
        "Click 4 KNOWN AXIS POINTS (ticks or corners)"
    )

    calib_data = []

    for i, (u, v) in enumerate(calib_pixels, 1):
        print("\n----------------------------------------")
        print(f"Calibration point {i}")
        print(f"Pixel location: ({u:.1f}, {v:.1f})")
        print("TYPE NUMBERS ONLY (examples: 0.1, 1, 10, 1e-8, 1e2)")

        xval = float(input("  Enter X value of this point: "))
        yval = float(input("  Enter Y value of this point: "))

        calib_data.append((xval, yval))

    # -------------------------
    # 3. Fit mapping
    # -------------------------
    xfit, yfit = fit_axis_mapping(calib_pixels, calib_data, axis_spec)

    # -------------------------
    # 4. Convert new data
    # -------------------------
    u_new, v_new = data_to_pixel(x_new, y_new, xfit, yfit, axis_spec)

    # -------------------------
    # 5. Plot overlay
    # -------------------------
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.imshow(img)
    ax.axis("off")

    if mode == "scatter":
        ax.scatter(u_new, v_new, s=markersize)
    else:
        order = np.argsort(u_new)
        ax.plot(u_new[order], v_new[order], linewidth=linewidth)

    plt.savefig(out_path, dpi=300, bbox_inches="tight", pad_inches=0)
    plt.show()

    print("\nOverlay complete.")
    print(f"Saved to: {out_path}")
