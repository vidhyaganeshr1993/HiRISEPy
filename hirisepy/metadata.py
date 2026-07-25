import re
import rasterio


def parse_hirise_filename(filename):
    """
    Extract HiRISE information from filename.

    Example:
    ESP_053039_1640_UNFILTERED_COLOR4.tif
    """

    name = str(filename)

    pattern = (
        r"(ESP|PSP)_"
        r"(\d+)_"
        r"(\d+)_"
        r"UNFILTERED_"
        r"(COLOR\d+)"
    )

    match = re.search(pattern, name)

    if match is None:
        raise ValueError(
            "Filename does not match HiRISE COLOR format"
        )

    phase_code = match.group(1)

    phase_names = {
        "ESP": "Extended Science Phase",
        "PSP": "Primary Science Phase"
    }

    metadata = {
        "science_phase_code": phase_code,
        "science_phase": phase_names[phase_code],
        "orbit": match.group(2),
        "target_code": match.group(3),
        "product_type": match.group(4),
    }

    return metadata

def get_spectral_metadata(filename):
    """
    Extract HiRISE band names and wavelengths.
    """

    with rasterio.open(filename) as src:

        tags = src.tags()

    band_names = []
    wavelengths = []

    for key, value in tags.items():

        if key.startswith("Band_"):

            # Example:
            # Band_1: NearInfrared (873.403381)

            match = re.search(
                r"(.+)\s\(([\d.]+)\)",
                value
            )

            if match:

                band_name = match.group(1)
                wavelength = float(match.group(2))

                band_names.append(band_name)
                wavelengths.append(wavelength)

    return {
        "band_names": band_names,
        "wavelengths": wavelengths
    }