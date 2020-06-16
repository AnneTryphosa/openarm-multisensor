#!/usr/bin/env python3
"""Utility functions for image processing algorithms.

This module contains functions used within image processing algorithms, such as
filters and edge detectors.
"""
import cv2
import numpy as np
import scipy

def get_filter_from_num(filter_type):
    """Map numbers to corresponding image filters.

    This function maps integer values to corresponding image filters for use in
    TODO. The mapping is as follows:
        1: median filter
        2: aggressive (fine) bilateral filter
        3: less aggressive (coarse) bilateral filter
        4: anisotropic diffusion filter
        other: no filter

    Args:
        filter_type (int): integer determining which filter to use

    Returns:
        image filter function that takes two arguments (img, run_params)
    """
    filter = None
    if filter_type == 1:
        filter = median_filter
    elif filter_type == 2:
        filter = fine_bilateral_filter
    elif filter_type == 3:
        filter = course_bilateral_filter
    elif filter_type == 4:
        filter = anisotropic_diffuse
    else:
        filter = no_filter
    return filter


# image filtering
def no_filter(img, run_params):
    """Applies no filter and converts image to grayscale (if color).

    Args:
        img (TODO type): image to be (potentially) grayscaled
        run_params (ParamValues): class containing values of parameters used in tracking

    Returns:
        TODO type grayscale, non-filtered version of input image
    """
    # check if image is color or grayscale, return grayscale version
    if len(img.shape) > 2:
        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        return img


def median_filter(img, run_params):
    """Applies a median filter to the given image.

    Args:
        img (TODO type): image to be filtered
        run_params (ParamValues): class containing values of parameters used in tracking

    Returns:
        TODO type median-filtered version of input image
    """

    kernelSize = 5
    return cv2.medianBlur(img, kernelSize)


def fine_bilateral_filter(img, run_params):
    """Applies an "aggressive" bilateral filter to the given image.

    Args:
        img (TODO type): image to be filtered
        run_params (ParamValues): class containing values of parameters used in tracking

    Returns:
        TODO type bilaterally-filtered version of input image
    """
    # convert to color (what bilateral filter expects)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # hyperparameters
    diam = run_params.fine_diam
    sigmaColor = run_params.fine_sigma_color
    sigmaSpace = run_params.fine_sigma_space
    bilateralColor = cv2.bilateralFilter(img, diam, sigmaColor, sigmaSpace)

    # convert back to grayscale and return
    return cv2.cvtColor(bilateralColor, cv2.COLOR_RGB2GRAY)


def course_bilateral_filter(img, run_params):
    """Applies a "less aggressive" bilateral filter to the given image.

    Args:
        img (TODO type): image to be filtered
        run_params (ParamValues): class containing values of parameters used in tracking

    Returns:
        TODO type bilaterally-filtered version of input image
    """
    # convert to color (what bilateral filter expects)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # hyperparameters
    diam = run_params.course_diam
    sigmaColor = run_params.course_sigma_color
    sigmaSpace = run_params.course_sigma_space
    bilateralColor = cv2.bilateralFilter(img, diam, sigmaColor, sigmaSpace)

    # convert back to grayscale and return
    return cv2.cvtColor(bilateralColor, cv2.COLOR_RGB2GRAY)

def anisotropic_diffuse(img, run_params):
    """Applies a Perona-Malik anisotropic diffusion filter to the given image.

    Args:
        img (TODO type): image to be filtered
        run_params (ParamValues): class containing values of parameters used in tracking

    Returns:
        TODO type anisotropic-diffused version of input image
    """
    # convert to color
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # hyperparameters
    alphaVar = 0.1
    KVar = 5
    nitersVar = 5
    diffusedColor = cv2.ximgproc.anisotropicDiffusion(src=img,
                                                      alpha=alphaVar,
                                                      K=KVar,
                                                      niters=nitersVar)

    # convert back to grayscale and return
    return cv2.cvtColor(diffusedColor, cv2.COLOR_RGB2GRAY)


def otsu_binarization(gray_image):
    """Applies Otsu binarization to the given image.

    Args:
        gray_img (TODO type): grayscale image to be binarized

    Returns:
        TODO type binarized version of input image
    """
    ret2, th2 = cv2.threshold(gray_image, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th2


def canny(gray_image):
    """Applies Canny edge detection to the given image.

    Args:
        gray_img (TODO type): grayscale image in which edges should be detected

    Returns:
        TODO type edges present in input image
    """

    edges = cv2.Canny(gray_image, 180, 200)
    return edges
