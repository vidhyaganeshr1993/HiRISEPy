"""
ISIS .cub to ENVI conversion utilities for HiRISEPy.
"""

import os
from osgeo import gdal

gdal.UseExceptions()


def convert_cub_to_envi(
    cub_file,
    output_directory
):
    """
    Convert ISIS .cub file to ENVI Float32 format.

    Equivalent to:

    gdal_translate -of ENVI -ot Float32 -unscale input.cub output.tif

    Parameters
    ----------
    cub_file : str
        Input ISIS cube.

    output_directory : str
        Folder for converted output.

    Returns
    -------
    str
        Path to converted TIFF.
    """


    os.makedirs(
        output_directory,
        exist_ok=True
    )


    base_name = os.path.splitext(
        os.path.basename(cub_file)
    )[0]


    output_tif = os.path.join(
        output_directory,
        base_name + ".tif"
    )


    print("Converting ISIS cube...")
    print("Input:", cub_file)
    print("Output:", output_tif)


    gdal.Translate(
        output_tif,
        cub_file,
        format="ENVI",
        outputType=gdal.GDT_Float32,
        unscale=True
    )


    print("Conversion complete!")


    return output_tif
    
def repair_hirise_header(
    tif_file
):
    """
    Repair ENVI header generated from ISIS cube.

    Adds HiRISE-specific metadata.
    """

    import os


    hdr_file = os.path.splitext(
        tif_file
    )[0] + ".hdr"


    print("Updating ENVI header...")
    print(hdr_file)


    with open(
        hdr_file,
        "r"
    ) as f:

        header = f.read()


    # Replace nodata value

    header = header.replace(
        "data ignore value = -32768",
        "data ignore value = -3.27680000e+04"
    )


    # Remove existing HiRISE metadata if present

    metadata_keys = [
        "wavelength",
        "map info",
        "projection info",
        "coordinate system string"
    ]


    lines = header.splitlines()

    clean_lines = []

    for line in lines:

        if not any(
            line.strip().startswith(key)
            for key in metadata_keys
        ):
            clean_lines.append(line)


    header = "\n".join(clean_lines)


    # Add fresh HiRISE metadata

    hirise_metadata = """

    wavelength = {873.403381, 691.897644, 502.560150}

    map info = {Mars Equirectangular Default, 1.0000, 1.0000, -0.2500, 0.2500, 5.0000000000e-01, 5.0000000000e-01, D_Unknown, units=Meters}

    projection info = {17, 3396190.0, 0.000000, 0.000000, 0.0, 0.0, D_Unknown, Mars Equirectangular Default, units=Meters}

    coordinate system string = {PROJCS["Mars Equirectangular Default",GEOGCS["GCS_Unknown",DATUM["D_Unknown",SPHEROID["S_Unknown",3396190.0,0.0]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Equidistant_Cylindrical"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],UNIT["Meter",1.0]]}

    """


    header += hirise_metadata




    with open(
        hdr_file,
        "w"
    ) as f:

        f.write(header)


    print("Header update complete!")
    
def prepare_hirise_cube(
    cub_file,
    output_directory
):
    """
    Complete ISIS cube preparation.

    Steps:
    1. Convert ISIS cube to ENVI TIFF
    2. Repair HiRISE-specific metadata

    Returns
    -------
    str
        Prepared TIFF file
    """


    tif_file = convert_cub_to_envi(
        cub_file,
        output_directory
    )


    repair_hirise_header(
        tif_file
    )


    print(
        "HiRISE cube preparation complete!"
    )


    return tif_file