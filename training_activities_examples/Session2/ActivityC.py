"""
ActivityC.py — image histograms, and edge detection

This example script shows how to:
 1) Create a histogram from a 2D array and plot this data
 2) Use cv2 to identify and plot edges at the air-tissue transition
"""

import numpy as np
import matplotlib.pyplot as plt
import pydicom
import cv2

import ActivityB

def create_histogram(image_array, bins=200, range=(-900, 1100)):
    """
    Compute histogram data for a CT image array.

    Inputs:
        image_array (np.ndarray): Image data in HU.
        bins (int): Number of histogram bins.
        range (tuple): HU range for histogram (default covers air to dense bone).
    Outputs:
        tuple: (hist_values, bin_edges)
    """
    hist_values, bin_edges = np.histogram(image_array, bins=bins, range=range)
    return hist_values, bin_edges

def plot_histogram(hist_values, bin_edges, title="CT Image Histogram"):
    """
    Plot histogram using computed values and bin edges.

    Inputs:
        hist_values (np.ndarray): Histogram counts.
        bin_edges (np.ndarray): Bin edges from np.histogram.
        title (str): Plot title.
    """
    plt.figure(figsize=(8, 5))
    plt.bar(bin_edges[:-1], hist_values, width=np.diff(bin_edges), color="steelblue", edgecolor="black")
    plt.title(title)
    plt.xlabel("Hounsfield Units (HU)")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.3)
    plt.show()

def detect_edges_canny_hu(img_hu, hu_range=(-900, 300), canny=(50, 150)):
    """
    Detect edges from a CT image (HU) using OpenCV Canny.

    Inputs:
        img_hu (np.ndarray): 2D CT image in Hounsfield Units.
        hu_range (tuple): (minHU, maxHU) window; values outside are clipped.
                          Default focuses on air (-900) to soft tissue (~0–300).
        canny (tuple): (low_threshold, high_threshold) for Canny in 8-bit space.
    Outputs:
        np.ndarray: 2D binary edge map (uint8), where 255 indicates an edge.
    """
    # 1) Window to focus edges near air-tissue transitions, then scale to 8-bit
    # because cv2.Canny expects uint8 images
    lo, hi = hu_range
    img_win = np.clip(img_hu, lo, hi)
    img8 = ((img_win - lo) / max(hi - lo, 1) * 255.0).astype(np.uint8)

    # 2) Canny edge detection (John Canny, 1986)
    edges = cv2.Canny(img8, canny[0], canny[1])
    return edges

if __name__ == "__main__":
    dicom_path = r"C:\your_path\import\CT_Anne_Dippet.dcm"
    ds = pydicom.dcmread(dicom_path)
    hu_image = ActivityB.rescale_to_hu(ds)

    # Create and plot histogram
    hist_values, bin_edges = create_histogram(hu_image)
    plot_histogram(hist_values, bin_edges)
    
    # Plot edges at the air-tissue transition
    edges = detect_edges_canny_hu(hu_image, hu_range=(-1000, 300), canny=(50, 150))
    ActivityB.plot_image(edges, title="Edges (Canny on HU)", cmap="gray")
