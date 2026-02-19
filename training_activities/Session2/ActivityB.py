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
if __name__ == "__main__":
    dicom_path = r"C:\Users\c4073711\Desktop\Ncl_STP_PracticalComputing\import\CT_Anne_Dippet.dcm"
    ds = pydicom.dcmread(dicom_path)

def plot_image(img, title="Image", cmap="gray"):
    plt.figure(figsize=(6, 6))
    plt.imshow(img, cmap=cmap)
    plt.axis("on")
    plt.title(title)
    plt.show()
plot_image(ds.pixel_array)

def rescale_to_hu(image):
    arr = image.pixel_array
    slope = getattr(ds, "RescaleSlope", 1.0)
    intercept = getattr(ds, "RescaleIntercept", 0.0)
    hu = arr * slope + intercept
    plot_image(hu)
    return hu
rescale_to_hu(ds)
    
    

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
    dicom_path = r"C:\Users\c4073711\Desktop\Ncl_STP_PracticalComputing\import\CT_Anne_Dippet.dcm"
    ds = pydicom.dcmread(dicom_path)