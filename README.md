# Figure Screenshot Overlay Tool

This project overlays new datasets onto existing figure screenshots
by calibrating pixel coordinates to data coordinates.

## How to use

1. Place your screenshot in `screenshots/`
2. Place your new dataset (CSV) in `data/`
3. Set axis scale + paths in `config.py`
4. Run `overlay_figure.py` in Spyder
5. Click:
   - plot box corners
   - 4 known axis points
6. Enter data values when prompted
7. Final figure is saved in `outputs/`

## Supported
- Linear / log axes
- High-DPI export
- Publication-quality overlays

## Notes
For skewed or perspective-distorted screenshots,
a homography-based version can be added.

