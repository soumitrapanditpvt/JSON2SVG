import os
import sys
import svgwrite
from SVG_Floorplan import SVG_Floorplan
import subprocess

def convert_svg_to_dxf(svg_file: str):
    """
    Converts the specified SVG file to a DXF file using Inkscape.
    :param svg_file: Path to the SVG file that needs to be converted.
    """
    # Generate the output DXF file name based on the SVG file name
    dxf_file = os.path.splitext(svg_file)[0] + ".dxf"
    print(f"Converting {svg_file} to {dxf_file} using Inkscape...")

    # Use subprocess to call the Inkscape command for conversion
    command = f"inkscape {svg_file} --export-filename={dxf_file}"
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully converted {svg_file} to {dxf_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")





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

    print(f"Current working directory: {os.getcwd()}")
    folder_path = os.path.abspath(folder_path)
    print(f"Absolute folder path: {folder_path}")
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist inside the container.")
        return
    # Look for any file with "floorplan" in its name and a .json extension
    floorplan_file = find_file_by_pattern(folder_path, "floorplan")
    sortplan_file = find_file_by_pattern(folder_path, "sortplan")  # Optional sortplan file

    if not floorplan_file:
        print(f"Floorplan file not found in {folder_path}. Skipping conversion.")
        return

    # Define the output SVG file name and path
    svg_file_path = os.path.join(folder_path,"output.svg")
    output_svg = svgwrite.Drawing(svg_file_path)
    output_svg.save()

    # Create an instance of your existing SVG_Floorplan converter
    # This should trigger the conversion during initialization itself.
    try:
        converter = SVG_Floorplan(floorplan_file=floorplan_file, output_file=os.path.join(folder_path,"output.svg"), sortplan_file=sortplan_file)
        print(f"SVG created and saved at {output_svg}")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

    # Convert the created SVG file to DXF using Inkscape
    #convert_svg_to_dxf(svg_file_path)






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