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
    threshold=0.005,
    relative_threshold=0.05
):
    """
    Check consistency of automatically selected
    dark pixel spectra.

    Parameters
    ----------
    dark_spectra : dict
        Output from extract_dark_spectra()

    threshold : float
        Maximum allowed absolute RMSE.

    relative_threshold : float
        Maximum allowed relative RMSE
        (fraction of mean signal, e.g. 0.05 = 5%).

    Returns
    -------
    dict
        QC status and message.
    """

    # Collect spectra

    spectra = []

    for band_name in sorted(dark_spectra.keys()):

        spectra.append(
            dark_spectra[band_name]["values"]
        )

    # Check for negative values

    for spectrum in spectra:

        if np.any(spectrum < 0):

            return {
                "status": "FAILED",
                "message":
                    "Negative values detected in dark spectra. "
                    "DS correction aborted."
            }

    # Pairwise comparisons

    pairwise_results = []

    maximum_rmse = 0.0
    maximum_relative_rmse = 0.0

    pair_names = [
        ("Spectrum 1", "Spectrum 2"),
        ("Spectrum 1", "Spectrum 3"),
        ("Spectrum 2", "Spectrum 3")
    ]

    pair_index = 0

    for i in range(len(spectra)):

        for j in range(i + 1, len(spectra)):

            rmse = calculate_spectral_rmse(
                spectra[i],
                spectra[j]
            )

            mean_signal = (
                np.mean(spectra[i]) +
                np.mean(spectra[j])
            ) / 2.0

            if mean_signal > 0:

                relative_rmse = rmse / mean_signal

            else:

                relative_rmse = np.inf

            pairwise_results.append({

                "pair": pair_names[pair_index],

                "rmse": rmse,

                "relative_rmse": relative_rmse

            })

            maximum_rmse = max(
                maximum_rmse,
                rmse
            )

            maximum_relative_rmse = max(
                maximum_relative_rmse,
                relative_rmse
            )

            pair_index += 1

    # Warning condition

    warning = (
        maximum_rmse > threshold
        or
        maximum_relative_rmse > relative_threshold
    )

    if warning:

        status = "WARNING"

        message = (
            f"Dark spectra consistency warning. "
            f"Maximum RMSE = {maximum_rmse:.5f} "
            f"(threshold = {threshold:.5f}); "
            f"Maximum Relative RMSE = "
            f"{maximum_relative_rmse*100:.2f}% "
            f"(threshold = {relative_threshold*100:.1f}%). "
            "Please verify selected dark pixels and DS correction."
        )

    else:

        status = "SUCCESS"

        message = (
            f"Dark spectra consistent. "
            f"Maximum RMSE = {maximum_rmse:.5f}; "
            f"Maximum Relative RMSE = "
            f"{maximum_relative_rmse*100:.2f}%."
        )

    return {

        "status": status,

        "message": message,

        "max_rmse": maximum_rmse,

        "max_relative_rmse": maximum_relative_rmse,

        "absolute_threshold": threshold,

        "relative_threshold": relative_threshold,

        "pairwise_results": pairwise_results

    }