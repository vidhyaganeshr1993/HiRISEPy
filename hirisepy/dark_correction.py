import numpy as np


def calculate_dark_offsets(
    dark_locations
):
    """
    Extract dark offsets for each band.

    Returns
    -------
    ndarray
        Dark offsets in band order:
        Band 1 (NIR)
        Band 2 (RED)
        Band 3 (BG)
    """

    offsets = np.array(
        [
            dark_locations["Band_1"]["value"],
            dark_locations["Band_2"]["value"],
            dark_locations["Band_3"]["value"]
        ],
        dtype=np.float32
    )

    return offsets



def apply_dark_correction(
    masked_image,
    dark_offsets
):
    """
    Apply additive dark subtraction.

    Parameters
    ----------
    masked_image : ndarray
        HiRISE cube:
        (bands, rows, cols)

    dark_offsets : ndarray
        One value per band

    Returns
    -------
    corrected_image : ndarray
    """

    corrected_image = np.empty_like(
        masked_image
    )


    for i in range(
        masked_image.shape[0]
    ):

        corrected_image[i] = (
            masked_image[i]
            -
            dark_offsets[i]
        )


    return corrected_image