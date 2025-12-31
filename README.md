
###     Overlay-New-Data-on-Published-Figures

Below is an example of an existing figure image (e.g. from a paper or report) before any new data is overlaid and the after.
![Original figure before overlay](output/Before.png)

This project provides a **reproducible Python workflow** for overlaying new data onto an existing figure image — including **published figures from papers, PDFs, theses, or reports** — even when the original plotting data is unavailable.

The figure is **calibrated once** by clicking known axis points.  
The calibration is saved to disk and reused indefinitely, allowing you to **replot, compare, and update overlays forever without clicking again**.

---

## Why this is useful

In research and engineering workflows, it is common to:
- Compare new experiments or simulations to **published figures**
- Reproduce or validate results from the literature
- Extend legacy plots when the original data is lost
- Work with figures extracted from PDFs or presentation slides

This tool turns a static figure image back into a **reusable plotting surface**, enabling accurate and scriptable comparisons.

---

## Key capabilities

- One-time interactive calibration using axis points  
- Save calibration to a JSON file for full reproducibility  
- Overlay and **compare new data directly against published figures**  
- Supports linear and logarithmic axes  
- Automatically clips overlays to the original figure range  
- Scriptable, batch-ready, and toolbox-quality  
- Produces publication-ready output using Matplotlib  

---

## Core idea

A plot image is just pixels.

By learning a mapping between  
**data space (x, y)** → **pixel space (u, v)**,  
new datasets can be overlaid accurately on top of an existing figure.

Once this mapping is calibrated, it never changes.

---

## Typical use cases

- Comparing new results to figures in journal papers  
- Reproducing plots when original data is unavailable  
- Validating models against published literature  
- Updating or extending legacy figures  
- Creating consistent visual comparisons across datasets  

