import numpy as np


def reorder_to_bgr_nir(
    image,
    metadata
):
    """
    Reorder HiRISE COLOR4 bands.

    Native HiRISE order:
        Band 1 = Near Infrared
        Band 2 = Red
        Band 3 = Blue-Green

    Output order:
        Band 1 = Blue-Green
        Band 2 = Red
        Band 3 = Near Infrared
    """

    # Reorder data cube
    reordered_image = image[
        [2, 1, 0],
        :, :
    ]


    # Copy metadata
    reordered_metadata = metadata.copy()


    # Update band names
    reordered_metadata["band_names"] = [
        "BlueGreen",
        "Red",
        "NearInfrared"
    ]


    # Update wavelengths
    reordered_metadata["wavelengths"] = [
        502.560150,
        691.897644,
        873.403381
    ]


    return (
        reordered_image,
        reordered_metadata
    )