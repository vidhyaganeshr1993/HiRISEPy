import os
import numpy as np
import spectral.io.envi as envi


def write_envi_product(
    image,
    metadata,
    output_directory,
    filename
):
    """
    Write corrected HiRISE cube as ENVI .img/.hdr.

    Parameters
    ----------
    image : numpy.ndarray
        Image cube in (bands, lines, samples)

    metadata : dict
        Metadata dictionary containing:
        - band_names
        - wavelengths

    output_directory : str
        Directory for ENVI output

    filename : str
        Output base filename (without extension)
    """

    os.makedirs(
        output_directory,
        exist_ok=True
    )


    output_path = os.path.join(
        output_directory,
        filename
    )


    print("Preparing ENVI export...")


    # Replace NaN pixels with HiRISE NoData value
    image_to_write = np.where(
        np.isnan(image),
        65535,
        image
    )


    # ENVI metadata
    envi_metadata = {

        "description":
            "DS corrected HiRISE COLOR4 product",

        "samples":
            image.shape[2],

        "lines":
            image.shape[1],

        "bands":
            image.shape[0],

        "interleave":
            "bil",

        "data type":
            4,   # float32

        "byte order":
            0,

        "band names":
            metadata["band_names"],

        "wavelength":
            metadata["wavelengths"],

        "wavelength units":
            "Nanometers",

        "data ignore value":
            65535
    }


    print("Writing ENVI files...")


    envi.save_image(
        output_path + ".hdr",

        image_to_write.transpose(
            1,
            2,
            0
        ),

        dtype=np.float32,

        metadata=envi_metadata,

        interleave="bil",

        force=True
    )


    print("Saved ENVI product:")
    print(output_path + ".hdr")
    print(output_path + ".img")


    return output_path