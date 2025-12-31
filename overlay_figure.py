"""
Overlay new data onto an existing figure screenshot
Author: Bernard

Calibrate once, replot forever.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# ==========================================================
# TOOLBOX FUNCTION
# ==========================================================
def overlay_data_on_figure(
    screenshot_path,
    x_new,
    y_new,
    *,
    xscale="linear",
    yscale="linear",
    n_cal_points=4,
    calibrate=True,
    calibration_file=None,
    out_path=None,
    line_kwargs=None,
):
    """
    Overlay new (x, y) data onto an existing figure screenshot.

    Parameters
    ----------
    calibrate : bool
        True  -> interactive calibration (click + input)
        False -> load calibration from calibration_file

    calibration_file : str
        Path to JSON file storing calibration parameters
    """

    if line_kwargs is None:
        line_kwargs = dict(color="m", linewidth=3)

    if calibration_file is None:
        raise ValueError("You must provide calibration_file")

    x_new = np.asarray(x_new, float)
    y_new = np.asarray(y_new, float)

    # -----------------------------
    # Helper for axis scaling
    # -----------------------------
    def _transform(v, scale):
        if scale == "log":
            return np.log10(v)
        return v

    # -----------------------------
    # Load screenshot
    # -----------------------------
    img = mpimg.imread(screenshot_path)

    # ==========================================================
    # CALIBRATION MODE
    # ==========================================================
    if calibrate or not os.path.exists(calibration_file):

        print("\n--- CALIBRATION MODE ---")

        fig_click, ax_click = plt.subplots(figsize=(10, 7))
        ax_click.imshow(img)
        ax_click.set_title(
            f"CLICK {n_cal_points} KNOWN AXIS POINTS\n"
            "(ticks or plot corners)"
        )
        ax_click.axis("off")

        pixel_pts = np.array(plt.ginput(n_cal_points, timeout=0))
        plt.close(fig_click)

        data_pts = []

        for i, (u, v) in enumerate(pixel_pts, start=1):
            print("\n----------------------------------------")
            print(f"Calibration point {i}")
            print(f"Pixel location: ({u:.1f}, {v:.1f})")
            print("Enter numeric values only (e.g. 0.1, 1, 10, 1e-8, 1e2)")

            xval = float(input("  X value at this point: "))
            yval = float(input("  Y value at this point: "))

            data_pts.append([xval, yval])

        data_pts = np.asarray(data_pts)

        # Fit pixel ↔ data mapping
        u = pixel_pts[:, 0]
        v = pixel_pts[:, 1]

        x = _transform(data_pts[:, 0], xscale)
        y = _transform(data_pts[:, 1], yscale)

        Ax = np.c_[x, np.ones_like(x)]
        Ay = np.c_[y, np.ones_like(y)]

        ax_, bx_ = np.linalg.lstsq(Ax, u, rcond=None)[0]
        ay_, by_ = np.linalg.lstsq(Ay, v, rcond=None)[0]

        xmin, xmax = data_pts[:, 0].min(), data_pts[:, 0].max()
        ymin, ymax = data_pts[:, 1].min(), data_pts[:, 1].max()

        calibration = dict(
            screenshot=screenshot_path,
            xscale=xscale,
            yscale=yscale,
            ax=ax_, bx=bx_,
            ay=ay_, by=by_,
            xmin=xmin, xmax=xmax,
            ymin=ymin, ymax=ymax,
        )

        os.makedirs(os.path.dirname(calibration_file), exist_ok=True)
        with open(calibration_file, "w") as f:
            json.dump(calibration, f, indent=2)

        print(f"\nCalibration saved to {calibration_file}")

    # ==========================================================
    # REPLAY MODE
    # ==========================================================
    else:
        print("\n--- REPLAY MODE ---")
        print(f"Loading calibration from {calibration_file}")

        with open(calibration_file, "r") as f:
            calibration = json.load(f)

        ax_ = calibration["ax"]
        bx_ = calibration["bx"]
        ay_ = calibration["ay"]
        by_ = calibration["by"]
        xmin, xmax = calibration["xmin"], calibration["xmax"]
        ymin, ymax = calibration["ymin"], calibration["ymax"]
        xscale = calibration["xscale"]
        yscale = calibration["yscale"]

    # ==========================================================
    # Clip new data to figure range
    # ==========================================================
    mask = (
        (x_new >= xmin) & (x_new <= xmax) &
        (y_new >= ymin) & (y_new <= ymax)
    )

    x_new = x_new[mask]
    y_new = y_new[mask]

    # ==========================================================
    # Convert new data → pixel space
    # ==========================================================
    x_t = _transform(x_new, xscale)
    y_t = _transform(y_new, yscale)

    u_new = ax_ * x_t + bx_
    v_new = ay_ * y_t + by_

    # ==========================================================
    # Render overlay
    # ==========================================================
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.imshow(img)
    ax.axis("off")

    order = np.argsort(u_new)
    ax.plot(u_new[order], v_new[order], **line_kwargs)

    if out_path is not None:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path, dpi=300, bbox_inches="tight", pad_inches=0)

    plt.show()
    return fig, ax


# ==========================================================
# TEST BLOCK (SAME SCRIPT)
# ==========================================================
if __name__ == "__main__":

    print("\nLoading test data...")
    x, y = np.loadtxt("data/new_dataset.csv", delimiter=",", unpack=True)

    overlay_data_on_figure(
        screenshot_path="data/sm13.png",
        x_new=x,
        y_new=y,
        xscale="log",
        yscale="log",
        calibrate=False,  # <<< CHANGE THIS
        calibration_file="output/sm13_calibration.json",
        out_path="output/overlay_result.png",
        line_kwargs=dict(color="m", linewidth=4),
    )
































# """
# Overlay new data onto an existing figure screenshot
# Author: Bernard
# """

# import os
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg


# # ==========================================================
# # TOOLBOX FUNCTION (KEEP THIS)
# # ==========================================================
# def overlay_data_on_figure(
#     screenshot_path,
#     x_new,
#     y_new,
#     *,
#     xscale="linear",
#     yscale="linear",
#     n_cal_points=4,
#     out_path=None,
#     line_kwargs=None,
# ):
#     """
#     Overlay new (x, y) data onto an existing figure screenshot
#     using interactive axis calibration.
#     """

#     if line_kwargs is None:
#         line_kwargs = dict(color="r", linewidth=3)

#     x_new = np.asarray(x_new, float)
#     y_new = np.asarray(y_new, float)

#     # -----------------------------
#     # Helper for axis scaling
#     # -----------------------------
#     def _transform(v, scale):
#         if scale == "log":
#             return np.log10(v)
#         return v

#     # -----------------------------
#     # Load screenshot
#     # -----------------------------
#     img = mpimg.imread(screenshot_path)

#     # -----------------------------
#     # Collect calibration clicks
#     # -----------------------------
#     fig_click, ax_click = plt.subplots(figsize=(10, 7))
#     ax_click.imshow(img)
#     ax_click.set_title(
#         f"CLICK {n_cal_points} KNOWN AXIS POINTS\n"
#         "(ticks or plot corners)"
#     )
#     ax_click.axis("off")

#     pixel_pts = plt.ginput(n_cal_points, timeout=0)
#     plt.close(fig_click)

#     pixel_pts = np.asarray(pixel_pts)

#     # -----------------------------
#     # Ask user for data values
#     # -----------------------------
#     data_pts = []

#     for i, (u, v) in enumerate(pixel_pts, start=1):
#         print("\n----------------------------------------")
#         print(f"Calibration point {i}")
#         print(f"Pixel location: ({u:.1f}, {v:.1f})")
#         print("Enter numeric values only (e.g. 0.1, 1, 10, 1e-8, 1e2)")

#         xval = float(input("  X value at this point: "))
#         yval = float(input("  Y value at this point: "))

#         data_pts.append([xval, yval])

#     data_pts = np.asarray(data_pts)

#     # -----------------------------
#     # Fit pixel ↔ data mapping
#     # -----------------------------
#     u = pixel_pts[:, 0]
#     v = pixel_pts[:, 1]

#     x = _transform(data_pts[:, 0], xscale)
#     y = _transform(data_pts[:, 1], yscale)

#     Ax = np.c_[x, np.ones_like(x)]
#     Ay = np.c_[y, np.ones_like(y)]

#     ax_, bx_ = np.linalg.lstsq(Ax, u, rcond=None)[0]
#     ay_, by_ = np.linalg.lstsq(Ay, v, rcond=None)[0]

#     # -----------------------------
#     # Infer axis limits (DATA SPACE)
#     # -----------------------------
#     xmin, xmax = data_pts[:, 0].min(), data_pts[:, 0].max()
#     ymin, ymax = data_pts[:, 1].min(), data_pts[:, 1].max()

#     # -----------------------------
#     # Clip new data to figure range
#     # -----------------------------
#     mask = (
#         (x_new >= xmin) & (x_new <= xmax) &
#         (y_new >= ymin) & (y_new <= ymax)
#     )

#     x_new = x_new[mask]
#     y_new = y_new[mask]

#     # -----------------------------
#     # Convert new data → pixel space
#     # -----------------------------
#     x_t = _transform(x_new, xscale)
#     y_t = _transform(y_new, yscale)

#     u_new = ax_ * x_t + bx_
#     v_new = ay_ * y_t + by_

#     # -----------------------------
#     # Render overlay
#     # -----------------------------
#     fig, ax = plt.subplots(figsize=(10, 7))
#     ax.imshow(img)
#     ax.axis("off")

#     order = np.argsort(u_new)
#     ax.plot(u_new[order], v_new[order], **line_kwargs)

#     if out_path is not None:
#         os.makedirs(os.path.dirname(out_path), exist_ok=True)
#         plt.savefig(out_path, dpi=300, bbox_inches="tight", pad_inches=0)

#     plt.show()

#     return fig, ax


# # ==========================================================
# # TEST BLOCK (SAFE TO REMOVE LATER)
# # ==========================================================
# if __name__ == "__main__":

#     print("\nLoading test data...")

#     # NOTE: no trailing space in filename!
#     x, y = np.loadtxt("data/new_dataset.csv", delimiter=",", unpack=True)

#     overlay_data_on_figure(
#         screenshot_path="data/sm13.png",
#         x_new=x,
#         y_new=y,
#         xscale="log",
#         yscale="log",
#         out_path="output/overlay_result.png",
#         line_kwargs=dict(color="red", linewidth=3),
#     )
