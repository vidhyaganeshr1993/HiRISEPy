import numpy as np
import matplotlib as plt

def local_stretch(image, lower=2, upper=98):
    """
    Apply percentile stretch for visualization.
    """

    import numpy as np

    vmin = np.nanpercentile(
        image,
        lower
    )

    vmax = np.nanpercentile(
        image,
        upper
    )

    stretched = (
        image - vmin
    ) / (
        vmax - vmin
    )

    stretched = np.clip(
        stretched,
        0,
        1
    )

    return stretched

def stretch_band(band, low=2, high=98):
    """
    Percentile stretch for visualization.

    Parameters
    ----------
    band : ndarray
        Single image band

    low : float
        Lower percentile

    high : float
        Upper percentile

    Returns
    -------
    stretched : ndarray
        Values scaled between 0 and 1
    """

    valid = band[np.isfinite(band)]

    vmin = np.percentile(valid, low)
    vmax = np.percentile(valid, high)

    stretched = (band - vmin) / (vmax - vmin)

    stretched = np.clip(
        stretched,
        0,
        1
    )

    return stretched.astype(np.float32)
    
def make_irb(image):
    """
    Create IRB false colour composite.

    R = NearInfrared
    G = Red
    B = BlueGreen
    """

    nir = stretch_band(image[0])

    red = stretch_band(image[1])

    blue_green = stretch_band(image[2])

    irb = np.dstack(
        [
            nir,
            red,
            blue_green
        ]
    )

    return irb
    
def show_image(image, title=None, figsize=(10, 8)):
    """
    Display an image with consistent formatting.

    Parameters
    ----------
    image : ndarray
        Image array

    title : str
        Plot title

    figsize : tuple
        Figure size
    """

    import matplotlib.pyplot as plt

    plt.figure(figsize=figsize)

    plt.imshow(image)

    if title is not None:
        plt.title(title)

    plt.axis("off")

    plt.show()
    
def plot_rois(
    image,
    rois,
    colors=None,
    marker_size=80,
    title="ROI locations"
):
    """
    Plot ROI locations on an image.

    Parameters
    ----------
    image : ndarray
        RGB/IRB image

    rois : dict
        Dictionary:
        {"ROI_name": (row, column)}

    colors : dict
        Dictionary:
        {"ROI_name": "color"}

    """

    import matplotlib.pyplot as plt


    plt.figure(figsize=(10,8))

    plt.imshow(image)


    for name, (row, col) in rois.items():

        color = None

        if colors is not None:
            color = colors[name]


        plt.scatter(
            col,
            row,
            s=marker_size,
            c=color,
            label=name
        )


    plt.legend()

    plt.title(title)

    plt.axis("off")

    plt.show()
    
def plot_dark_spectra(
    spectra
):
    """
    Plot I/F spectra extracted from darkest pixel locations.

    HiRISE COLOR band order:
    Band 1 = NearInfrared  (873.403381 nm)
    Band 2 = Red           (691.897644 nm)
    Band 3 = BlueGreen     (502.560150 nm)

    Spectra are reordered for plotting:
    BlueGreen -> Red -> NearInfrared
    """

    import matplotlib.pyplot as plt
    import numpy as np


    wavelengths = np.array([
        502.560150,
        691.897644,
        873.403381
    ])


    band_order = [
        2,  # BlueGreen
        1,  # Red
        0   # NearInfrared
    ]


    colors = {
        "Band_1": "magenta",
        "Band_2": "red",
        "Band_3": "blue"
    }


    labels = {
        "Band_1": "NIR minimum pixel",
        "Band_2": "RED minimum pixel",
        "Band_3": "BG minimum pixel"
    }


    plt.figure(
        figsize=(8,5)
    )


    for name, data in spectra.items():

        values = data["values"]

        ordered_values = values[band_order]


        plt.plot(
            wavelengths,
            ordered_values,
            marker="o",
            color=colors[name],
            label=labels[name]
        )


    plt.xlabel(
        "Wavelength (nm)"
    )

    plt.ylabel(
        "I/F"
    )

    plt.title(
        "Dark Pixel I/F Spectra"
    )

    plt.legend()

    plt.grid()

    plt.show()
    
def plot_dark_pixel_zoom_irb(
    irb,
    dark_locations,
    window_size=100
):
    """
    Plot zoomed IRB regions around darkest pixels.

    Parameters
    ----------
    irb : ndarray
        IRB image
        Shape:
        (rows, columns, 3)

    dark_locations : dict
        Output from find_dark_pixels()

    window_size : int
        Size of zoom window
    """

    import matplotlib.pyplot as plt


    names = {
        "Band_1": "NIR minimum pixel",
        "Band_2": "RED minimum pixel",
        "Band_3": "BG minimum pixel"
    }


    colors = {
        "Band_1": "magenta",
        "Band_2": "red",
        "Band_3": "blue"
    }


    for band_name, location in dark_locations.items():

        row = location["row"]
        col = location["col"]
        value = location["value"]


        half = window_size // 2


        row_min = max(
            row-half,
            0
        )

        row_max = min(
            row+half,
            irb.shape[0]
        )


        col_min = max(
            col-half,
            0
        )

        col_max = min(
            col+half,
            irb.shape[1]
        )


        crop = irb[
            row_min:row_max,
            col_min:col_max
        ]


        plt.figure(
            figsize=(6,6)
        )


        plt.imshow(
            crop
        )


        plt.scatter(
            col-col_min,
            row-row_min,
            s=120,
            c=colors[band_name],
            marker="x",
            linewidths=3
        )


        plt.title(
            f"{names[band_name]}\n"
            f"Row={row}, Col={col}\n"
            f"I/F={value:.6f}"
        )


        plt.axis("off")


        plt.show()
        
def create_dark_pixel_qc_report(
    irb,
    masked_image,
    dark_locations,
    dark_spectra,
    filename=None,
    qc_directory=None,
    window_size=100
):
    """
    Create and optionally save a HiRISE dark pixel QC report.

    Includes:
    - Full IRB image with dark pixel locations
    - Zoomed IRB views
    - Dark pixel I/F spectra
    - Summary table

    Parameters
    ----------
    irb : ndarray
        IRB composite image

    masked_image : ndarray
        Masked HiRISE image cube

    dark_locations : dict
        Output from find_dark_pixels()

    dark_spectra : dict
        Output from extract_dark_spectra()

    filename : str
        Original input filename

    qc_directory : str
        Directory where QC PNG will be saved

    window_size : int
        Size of zoom window
    """

    import matplotlib.pyplot as plt
    import os


    colors = {
        "Band_1": "magenta",
        "Band_2": "red",
        "Band_3": "blue"
    }


    labels = {
        "Band_1": "NIR minimum pixel",
        "Band_2": "RED minimum pixel",
        "Band_3": "BG minimum pixel"
    }


    # ---------------------------------
    # Create automatic save path
    # ---------------------------------

    save_path = None

    if filename is not None and qc_directory is not None:

        os.makedirs(
            qc_directory,
            exist_ok=True
        )

        base = os.path.splitext(
            os.path.basename(filename)
        )[0]

        save_path = os.path.join(
            qc_directory,
            base + "_dark_pixel_QC.png"
        )


    # ---------------------------------
    # Create figure
    # ---------------------------------

    fig = plt.figure(
        figsize=(15,14)
    )


    # ---------------------------------
    # Full IRB image
    # ---------------------------------

    ax1 = plt.subplot2grid(
        (4,3),
        (0,0),
        colspan=3
    )


    ax1.imshow(irb)


    for band_name, loc in dark_locations.items():

        ax1.scatter(
            loc["col"],
            loc["row"],
            s=120,
            marker="x",
            linewidths=3,
            c=colors[band_name],
            label=labels[band_name]
        )


    ax1.set_title(
        "HiRISE IRB Image - Dark Pixel Locations"
    )

    ax1.legend()

    ax1.axis("off")


    # ---------------------------------
    # IRB zoom panels
    # ---------------------------------

    for i, (band_name, loc) in enumerate(
        dark_locations.items()
    ):

        ax = plt.subplot2grid(
            (4,3),
            (1,i)
        )


        row = loc["row"]
        col = loc["col"]


        half = window_size // 2


        row_min = max(
            row-half,
            0
        )

        row_max = min(
            row+half,
            irb.shape[0]
        )


        col_min = max(
            col-half,
            0
        )

        col_max = min(
            col+half,
            irb.shape[1]
        )


        crop = irb[
            row_min:row_max,
            col_min:col_max
        ]


        crop_stretched = local_stretch(
            crop
        )


        ax.imshow(
            crop_stretched
        )


        ax.scatter(
            col-col_min,
            row-row_min,
            s=100,
            marker="x",
            linewidths=3,
            c=colors[band_name]
        )


        ax.set_title(
            labels[band_name] + "\n(local stretch)"
        )

        ax.axis("off")


    # ---------------------------------
    # Spectrum plot
    # ---------------------------------

    ax3 = plt.subplot2grid(
        (4,3),
        (2,0),
        colspan=3
    )


    wavelengths = [
        502.560150,
        691.897644,
        873.403381
    ]


    order = [
        2,
        1,
        0
    ]


    for band_name, data in dark_spectra.items():

        ax3.plot(
            wavelengths,
            data["values"][order],
            marker="o",
            color=colors[band_name],
            label=labels[band_name]
        )


    ax3.set_xlabel(
        "Wavelength (nm)"
    )

    ax3.set_ylabel(
        "I/F"
    )

    ax3.set_title(
        "Dark Pixel I/F Spectra"
    )

    ax3.grid()

    ax3.legend()


    # ---------------------------------
    # Summary table
    # ---------------------------------

    ax4 = plt.subplot2grid(
        (4,3),
        (3,0),
        colspan=3
    )

    ax4.axis("off")


    table_data = []


    for band_name, loc in dark_locations.items():

        table_data.append(
            [
                labels[band_name],
                loc["row"],
                loc["col"],
                f"{loc['value']:.6f}"
            ]
        )


    table = ax4.table(
        cellText=table_data,
        colLabels=[
            "Pixel",
            "Row",
            "Column",
            "I/F"
        ],
        loc="center",
        cellLoc="center"
    )


    table.auto_set_font_size(False)

    table.set_fontsize(10)

    table.scale(
        1,
        1.5
    )


    plt.tight_layout()


    # ---------------------------------
    # Save QC figure
    # ---------------------------------

    if save_path is not None:

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

        print(
            f"QC report saved: {save_path}"
        )


    plt.show()
    
def create_dark_correction_qc_report(
    irb_before,
    irb_after,
    masked_image_before,
    corrected_image,
    dark_locations,
    filename,
    qc_directory
):

    import os
    import matplotlib.pyplot as plt
    import numpy as np


    fig = plt.figure(
        figsize=(14, 10)
    )


    # -----------------------------
    # Original IRB
    # -----------------------------

    ax1 = plt.subplot(2, 2, 1)

    ax1.imshow(
        irb_before
    )

    ax1.set_title(
        "Original IRB"
    )

    ax1.axis("off")


    # -----------------------------
    # Corrected IRB
    # -----------------------------

    ax2 = plt.subplot(2, 2, 2)

    ax2.imshow(
        irb_after
    )

    ax2.set_title(
        "Dark corrected IRB"
    )

    ax2.axis("off")


    # -----------------------------
    # Spectrum comparison
    # -----------------------------

    ax3 = plt.subplot(2, 1, 2)


    wavelengths = np.array(
        [
            873.403381,
            691.897644,
            502.560150
        ]
    )


    for name, location in dark_locations.items():

        band_index = int(
            name.split("_")[1]
        ) - 1


        row = location["row"]
        col = location["col"]


        before = masked_image_before[
            :,
            row,
            col
        ]


        after = corrected_image[
            :,
            row,
            col
        ]


        ax3.plot(
            wavelengths,
            before,
            marker="o",
            label=f"{name} before"
        )


        ax3.plot(
            wavelengths,
            after,
            marker="x",
            linestyle="--",
            label=f"{name} corrected"
        )


    ax3.set_xlabel(
        "Wavelength (nm)"
    )

    ax3.set_ylabel(
        "I/F"
    )

    ax3.set_title(
        "Dark pixel spectra before and after correction"
    )

    ax3.legend()


    plt.tight_layout()

    base_name = os.path.basename(
        filename
    )
    
    base_name = base_name.replace(
        ".tif",
        "_DS_QC.png"
    )
    
    output = os.path.join(
        str(qc_directory),
        str(base_name)
        
    )

    print("DEBUG filename:", filename)
    print("DEBUG qc_directory:", qc_directory)
    print("DEBUG output:", output)
    print("Saving DS QC to:", output)

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )


    plt.close()


    return output