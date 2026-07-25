import numpy as np


def find_dark_pixels(image):
    """
    Find darkest pixel location independently for each band.

    Parameters
    ----------
    image : ndarray
        Shape (bands, rows, columns)

    Returns
    -------
    dark_locations : dict
        Pixel location for each band
    """

    dark_locations = {}

    for band in range(image.shape[0]):

        band_data = image[band]

        # Ignore NaN pixels
        dark_index = np.nanargmin(band_data)

        row, col = np.unravel_index(
            dark_index,
            band_data.shape
        )

        dark_locations[f"Band_{band+1}"] = {
            "row": row,
            "col": col,
            "value": band_data[row, col]
        }

    return dark_locations
    
def extract_dark_spectra(image, dark_locations):
    """
    Extract spectra from darkest pixel locations.

    Parameters
    ----------
    image : ndarray
        Shape (bands, rows, columns)

    dark_locations : dict
        Output from find_dark_pixels()

    Returns
    -------
    spectra : dict
    """

    spectra = {}

    for band_name, location in dark_locations.items():

        band_number = int(
            band_name.split("_")[1]
        ) - 1

        row = location["row"]
        col = location["col"]

        spectrum = image[:, row, col]

        spectra[band_name] = {
            "row": row,
            "col": col,
            "values": spectrum
        }

    return spectra