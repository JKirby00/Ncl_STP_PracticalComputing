"""
ActivityB.py — CT DICOM plotting, HU rescaling, and windowing presets

In this activity you will write functions to:
 1) Load a DICOM file with pydicom, and plot the image
 2) Rescale stored pixel values to Hounsfield Units (HU)
 3) Apply common windowing presets (lung, soft tissue, bone)
"""

import numpy as np
import matplotlib.pyplot as plt
import pydicom

def plot_image(img, title="Image", cmap="gray"):
    """
    Display a 2D image array using Matplotlib with optional title and colormap.

    Inputs:
        img (np.ndarray): 2D array representing the image to display.
        title (str, optional): Figure title. Defaults to "Image".
        cmap (str, optional): Matplotlib colormap name (e.g., "gray"). Defaults to "gray".
    Outputs:
        None: Shows the plot in a window (side effect).
    """
    pass

def rescale_to_hu(ds):
    """
    Convert DICOM pixel data to Hounsfield Units (HU) using slope and intercept.

    Inputs:
        ds (pydicom.dataset.FileDataset): DICOM dataset containing pixel data and
            optional RescaleSlope and RescaleIntercept tags.
    Outputs:
        np.ndarray: Image array in Hounsfield Units (same shape as ds.pixel_array).
    """
    pass

def window_image(img_hu, preset=None):
    """
    Apply CT windowing based on preset (center, width) and normalize to [0, 1].

    Inputs:
        img_hu (np.ndarray): HU image array to window.
        preset (str or None, optional): Window preset name. Supported values:
            "lung", "soft tissue", "bone", "default", or None.
            If "default" or None, returns the original img_hu (no windowing).
    Outputs:
        np.ndarray: Windowed image array in [0, 1] for display, or original HU array
        if no windowing is applied.
    """
    pass

if __name__ == "__main__":
    dicom_path = r"C:\your_path\import\CT_Anne_Dippet.dcm"
    ds = pydicom.dcmread(dicom_path)