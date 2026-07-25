from pathlib import Path
import rasterio
from hirisepy.metadata import (parse_hirise_filename, get_spectral_metadata)


def read_hirise_color_image(filename):
    """
    Read a HiRISE unfiltered COLOR4/COLOR5 image.

    Parameters
    ----------
    filename : str or Path
        Input HiRISE .tif file

    Returns
    -------
    image : numpy.ndarray
        Image cube with shape (bands, rows, columns)

    metadata : dict
        Image metadata
    """

    filename = Path(filename)

    with rasterio.open(filename) as src:

        # Read all image bands
        image = src.read()

        # Store raster metadata
        metadata = {
            "filename": filename.name,
            "path": str(filename),
            "bands": src.count,
            "height": src.height,
            "width": src.width,
            "dtype": src.dtypes,
            "nodata": src.nodata,
            "crs": src.crs,
            "transform": src.transform,
        }

    # Add HiRISE filename information
    metadata.update(
        parse_hirise_filename(filename.name)
    )
    metadata.update(
        get_spectral_metadata(filename)
    )
    
    return image, metadata