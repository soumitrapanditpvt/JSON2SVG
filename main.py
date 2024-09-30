import os
import sys
from SVG_Floorplan import SVG_Floorplan

def find_file_by_pattern(folder_path, pattern):
    """
    Find a file in the given folder that matches the specified pattern.

    Args:
        folder_path (str): The folder to search in.
        pattern (str): The substring pattern to look for in file names.

    Returns:
        str: The first file name that matches the pattern, or None if no match is found.
    """
    for file_name in os.listdir(folder_path):
        if pattern in file_name and file_name.endswith(".json"):
            return os.path.join(folder_path, file_name)
    return None

def convert_folder(folder_path):
    """
    Wrapper function to process a given folder and run the SVG_Floorplan converter.

    Args:
        folder_path (str): Path to the folder containing floorplan and optionally sortplan files.
    """
    # Look for any file with "floorplan" in its name and a .json extension
    floorplan_file = find_file_by_pattern(folder_path, "floorplan")
    sortplan_file = find_file_by_pattern(folder_path, "sortplan")  # Optional sortplan file

    if not floorplan_file:
        print(f"Floorplan file not found in {folder_path}. Skipping conversion.")
        return

    # Define the output SVG file name and path
    output_svg = os.path.join(folder_path, "output.svg")

    # Create an instance of your existing SVG_Floorplan converter
    # This should trigger the conversion during initialization itself.
    try:
        converter = SVG_Floorplan(floorplan_file, output_svg, sortplan_file)
        print(f"SVG created and saved at {output_svg}")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

if __name__ == "__main__":
    # The first argument should be the folder path
    if len(sys.argv) < 2:
        print("Usage: python converter_wrapper.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print(f"Specified folder path {folder_path} does not exist.")
        sys.exit(1)

    # Call the convert_folder function with the provided folder path
    convert_folder(folder_path)