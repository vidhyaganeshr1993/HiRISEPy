import os

from hirisepy.io import read_hirise_color_image

from hirisepy.masking import (
    create_common_mask,
    apply_common_mask
)

from hirisepy.dark_pixels import (
    find_dark_pixels,
    extract_dark_spectra
)

from hirisepy.dark_correction import (
    calculate_dark_offsets,
    apply_dark_correction
)

from hirisepy.visualization import (
    make_irb,
    create_dark_pixel_qc_report,
    create_dark_correction_qc_report
)

from hirisepy.band_stacking import reorder_to_bgr_nir
from hirisepy.envi_io import write_envi_product


def process_hirise_file(
    filename,
    qc_directory,
    output_directory
):
    """
    Complete HiRISE dark pixel QC workflow.

    Parameters
    ----------
    filename : str
        Input HiRISE COLOR TIFF

    qc_directory : str
        Folder for QC outputs

    Returns
    -------
    metadata
    dark_locations
    """


    print("Reading image...")


    image, metadata = read_hirise_color_image(
        filename
    )


    print("Creating mask...")


    mask = create_common_mask(
        image,
        metadata["nodata"]
    )


    masked_image = apply_common_mask(
        image,
        mask
    )


    print("Creating IRB...")


    irb = make_irb(
        masked_image
    )
    

    print("Finding dark pixels...")


    dark_locations = find_dark_pixels(
        masked_image
    )
    
    # Check for negative minima values

    for band_name, values in dark_locations.items():

        if values["value"] < 0:

            raise ValueError(
            "DS correction not possible - negative minima values"
            )


    print("Extracting spectra...")


    dark_spectra = extract_dark_spectra(
        masked_image,
        dark_locations
    )
    
    print("Calculating dark offsets...")


    dark_offsets = calculate_dark_offsets(
    dark_locations
    )


    print("Applying dark correction...")


    corrected_image = apply_dark_correction(
        masked_image,
        dark_offsets
    )
    
    print("Creating corrected IRB...")
    irb_corrected = make_irb(
        corrected_image
    )
    
    
    
    


    print("Creating QC report...")


    create_dark_pixel_qc_report(
        irb,
        masked_image,
        dark_locations,
        dark_spectra,
        filename=filename,
        qc_directory=qc_directory
    )
    
    print("QC directory is:", qc_directory)
    
    create_dark_correction_qc_report(
        irb,
        irb_corrected,
        masked_image,
        corrected_image,
        dark_locations,
        filename,
        qc_directory
    )


    print("Reordering bands...")

    reordered_image, reordered_metadata = reorder_to_bgr_nir(
        corrected_image,
        metadata
    )
    
    print("Reordered metadata:")
    print(reordered_metadata["band_names"])
    print(reordered_metadata["wavelengths"])
    
    print("Writing ENVI product...")

    base_name = os.path.splitext(
        os.path.basename(filename)
    )[0]


    output_name = (
        base_name +
        "_DS_CORRECTED"
    )


    write_envi_product(
        reordered_image,
        reordered_metadata,
        output_directory,
        output_name
    )
    
    
    print("Processing complete!")


    return (
        reordered_metadata,
        dark_locations,
        reordered_image,
        dark_offsets
    )