"""
ActivityB.py — CT DICOM plotting, HU rescaling, and windowing presets

This example script shows how to:
 1) Load a DICOM file with pydicom and plot the image
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
    plt.figure(figsize=(6, 6))
    plt.imshow(img, cmap=cmap)
    plt.title(title)
    plt.axis("off")
    plt.colorbar(shrink=0.7)
    plt.tight_layout()
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
    arr = ds.pixel_array
    slope = getattr(ds, "RescaleSlope", 1.0)
    intercept = getattr(ds, "RescaleIntercept", 0.0)
    hu = arr * slope + intercept
    return hu

def window_image(img_hu, preset="default"):
    """
    Apply CT windowing based on preset (center, width) and normalize to [0, 1].

    Inputs:
        img_hu (np.ndarray): HU image array to window.
        preset (str): Window preset name. Supported values:
            "lung", "soft tissue", "bone", or "default".
            If "default", returns the original img_hu (no windowing).
    Outputs:
        np.ndarray: Windowed image for display, or original HU array
        if no windowing is applied.
    """
    # Common CT window presets (center, width)
    window_presets = {
        "lung": (-600, 1500),
        "soft tissue": (40, 400),
        "bone": (300, 1500),
        "default": None,
    }
    # Default behavior: no windowing (return original HU)
    if preset == "default":
        return img_hu

    if preset not in window_presets:
        raise ValueError(
            f"Invalid preset '{preset}'. Choose one of: {', '.join(window_presets.keys())}"
        )

    center, width = window_presets[preset]
    lower = center - (width / 2.0)
    upper = center + (width / 2.0)

    windowed = np.clip(img_hu, lower, upper)
    return windowed

if __name__ == "__main__":
    dicom_path = r"C:\your_path\import\CT_Anne_Dippet.dcm"
    ds = pydicom.dcmread(dicom_path)

    # Plot stored pixel data
    stored = ds.pixel_array
    plot_image(stored, title="Stored pixel values (as read)")

    # Rescale to HU if CT
    modality = getattr(ds, "Modality", "").upper()
    if modality == "CT":
        img_hu = rescale_to_hu(ds)
        plot_image(img_hu, title="CT image in Hounsfield Units (HU)")

        # Apply window presets and plot
        window_presets = ['soft tissue', 'lung', 'bone']
        for preset in window_presets:
            win = window_image(img_hu, preset)
            plot_image(win, title=f"Windowed: {preset}")