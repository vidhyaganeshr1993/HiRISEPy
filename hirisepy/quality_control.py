import numpy as np


def calculate_spectral_rmse(spec1, spec2):
    """
    Calculate RMSE between two spectra.
    """

    return np.sqrt(
        np.mean(
            (spec1 - spec2) ** 2
        )
    )
    
def validate_dark_spectra(
    dark_spectra,
    threshold=0.005
):
    """
    Check consistency of automatically selected
    dark pixel spectra.

    Parameters
    ----------
    dark_spectra : dict
        Output from extract_dark_spectra()

    threshold : float
        Maximum allowed RMSE before warning

    Returns
    -------
    dict
        QC status and message
    """


    # Collect spectra

    spectra = []

    for band_name in sorted(dark_spectra.keys()):

        spectrum = dark_spectra[band_name]["values"]

        spectra.append(spectrum)


    # Check for negative values

    for spectrum in spectra:

        if np.any(spectrum < 0):

            return {
                "status": "FAILED",
                "message":
                "Negative values detected in dark spectra. "
                "DS correction aborted."
            }


    # Calculate pairwise RMSE

    rmses = []

    for i in range(len(spectra)):

        for j in range(i + 1, len(spectra)):

            rmse = calculate_spectral_rmse(
                spectra[i],
                spectra[j]
            )

            rmses.append(rmse)


    maximum_rmse = max(rmses)
    
    mean_signal = np.mean(
        [
            np.mean(spectrum)
            for spectrum in spectra
        ]
    )


    relative_rmse = (
        maximum_rmse /
        mean_signal
    )    


    # Warning condition

    if maximum_rmse > threshold:

        return {
            "status": "WARNING",
            "message":
            f"Dark spectra RMSE ({maximum_rmse:.5f}) "
            f"is greater than threshold ({threshold}). "
            "Please verify DS correction results.",
            "max_rmse": maximum_rmse,
            "relative_rmse": relative_rmse,
            "threshold": threshold,
            "pairwise_rmse":rmses
        }


    # Everything is good

    return {
        "status": "SUCCESS",
        "message":
        f"Dark spectra consistent "
        f"(RMSE={maximum_rmse:.5f}).",
        "max_rmse": maximum_rmse,
        "relative_rmse": relative_rmse,
        "threshold": threshold,
        "pairwise_rmse":rmses
    }