"""
ActivityB.py — CT DICOM plotting, HU rescaling, and windowing presets

In this activity you will write functions to:
 1) Load a DICOM file with pydicom, and plot the image
 2) Rescale stored pixel values to Hounsfield Units (HU)
 3) Apply common windowing presets (lung, soft tissue, bone)
"""

import numpy as np
import matplotlib.pyplot as plt
import pydicom as dcm

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

    fig, ax = plt.subplots()
    ax.imshow(image_data, cmap = cmap)
    ax.set_title(title)
    plt.show()

def rescale_to_hu(ds):
    """
    Convert DICOM pixel data to Hounsfield Units (HU) using slope and intercept.

    Inputs:
        ds (pydicom.dataset.FileDataset): DICOM dataset containing pixel data and
            optional RescaleSlope and RescaleIntercept tags.
    Outputs:
        np.ndarray: Image array in Hounsfield Units (same shape as ds.pixel_array).
    """

    ct_array = ds.pixel_array
    slope = getattr(ds, "RescaleSlope", 1.0)
    intercept = getattr(ds, "RescaleIntercept", 0.0)
    hu_array = ct_array * slope + intercept
    
    return hu_array


def window_image(img_hu, preset="default"):
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

     # Common CT window presets (center, width)
    window_presets = {
        "lung": (-600, 1500),
        "soft tissue": (40, 400),
        "bone": (300, 1500),
        "default": None,
    }

    if preset == "default":
        return img_hu
    
    center, width = window_presets[preset]
    lower = center - (width / 2.0)
    upper = center + (width / 2.0)

    windowed = np.clip(img_hu, lower, upper)
    return windowed


if __name__ == "__main__":
    dicom_path = r"C:\Users\b1021924\Desktop\scientificComputingSession1\Ncl_STP_PracticalComputing\import\CT_Anne_Dippet.dcm"
    ds = dcm.dcmread(dicom_path)
    image_data = ds.pixel_array

    plot_image(image_data)
    
    img_hu = rescale_to_hu(ds)
    plot_image(img_hu, "Rescaled")

    img_window = window_image(ds, "bone")
    plot_image(img_window, "Windowed")
