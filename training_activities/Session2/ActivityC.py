"""
ActivityC.py — image histograms, and edge detection

In this activity you will write functions to:
 1) Create a histogram from a 2D array and how to plot this data
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
    pass

def plot_histogram(hist_values, bin_edges, title="CT Image Histogram"):
    """
    Plot histogram using computed values and bin edges.

    Inputs:
        hist_values (np.ndarray): Histogram counts.
        bin_edges (np.ndarray): Bin edges from np.histogram.
        title (str): Plot title.
    """
    pass

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
    pass

if __name__ == "__main__":
    dicom_path = r"A:\STPComputing\import\Anne Dippet\CT1.2.752.243.1.1.20260108132323816.6100.12002.dcm"
    ds = pydicom.dcmread(dicom_path)