import os
import csv

from hirisepy.pipeline import process_hirise_file


def process_hirise_folder(
    input_directory,
    qc_directory,
    corrected_directory,
    summary_file=None
):
    """
    Process all HiRISE COLOR TIFF files in a folder.

    Parameters
    ----------
    input_directory : str
        Folder containing HiRISE TIFF files

    qc_directory : str
        Folder for QC reports

    corrected_directory : str
        Folder for DS corrected ENVI products

    summary_file : str, optional
        CSV summary output
    """


    # Find all TIFF files

    files = []

    for filename in os.listdir(input_directory):

        if filename.lower().endswith(".tif"):

            files.append(
                os.path.join(
                    input_directory,
                    filename
                )
            )


    print(
        f"Found {len(files)} HiRISE files"
    )


    results = []


    # Process each file

    for i, filepath in enumerate(files):

        print("\n-----------------------------")
        print(
            f"Processing {i+1}/{len(files)}"
        )
        print(
            os.path.basename(filepath)
        )
        print("-----------------------------")


        try:

            print(
                "Starting full pipeline..."
            )


            metadata, dark_locations, corrected_image, dark_offsets = process_hirise_file(
                filepath,
                qc_directory,
                corrected_directory
            )


            results.append(
                {
                    "filename": os.path.basename(filepath),
                    "status": "SUCCESS",
                    "error_message": "",

                    "science_phase": metadata.get(
                        "science_phase",
                        ""
                    ),

                    "orbit": metadata.get(
                        "orbit",
                        ""
                    ),

                    "target_code": metadata.get(
                        "target_code",
                        ""
                    ),

                    "NIR_min_IF": dark_locations["Band_1"]["value"],

                    "RED_min_IF": dark_locations["Band_2"]["value"],

                    "BG_min_IF": dark_locations["Band_3"]["value"]
                }
            )


        except Exception as e:
            
            error_message = str(e)

            print(
                "FAILED:",
                error_message
            )
            
            if "negative minima values" in error_message:
                
                    status = "FAILED_DS_NEGATIVE_MINIMA"
                    
            else:
                
                status = "FAILED ERROR"
                 


            results.append(
                {
                    "filename": os.path.basename(filepath),
                    "status": status,
                    "error_message": error_message,
                    "science_phase": "",
                    "orbit": "",
                    "target_code": "",
                    "NIR_min_IF": "",
                    "RED_min_IF": "",
                    "BG_min_IF": ""
                }
            )


    # Write summary CSV

    if summary_file is not None:

        with open(
            summary_file,
            "w",
            newline=""
        ) as f:

            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "filename",
                    "status",
                    "error_message",
                    "science_phase",
                    "orbit",
                    "target_code",
                    "NIR_min_IF",
                    "RED_min_IF",
                    "BG_min_IF"
                ]
            )

            writer.writeheader()

            writer.writerows(results)


        print(
            f"\nSummary saved: {summary_file}"
        )


    return results