import numpy as np


def create_common_mask(image, nodata_value):
    """
    Create one common mask for all bands.

    A pixel is marked invalid if ANY band contains the NoData value.

    Parameters
    ----------
    image : ndarray
        Shape (bands, rows, columns)

    nodata_value : number

    Returns
    -------
    common_mask : ndarray (bool)
    """

    common_mask = np.any(
        image == nodata_value,
        axis=0
    )

    return common_mask
    
def apply_common_mask(image, common_mask):
    """
    Replace invalid pixels with NaN in all bands.

    Parameters
    ----------
    image : ndarray
        Shape (bands, rows, columns)

    common_mask : ndarray
        Boolean mask

    Returns
    -------
    masked_image : ndarray
    """

    masked_image = image.astype(np.float32).copy()

    masked_image[:, common_mask] = np.nan

    return masked_image