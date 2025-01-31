import os
from pathlib import Path


def convert_to_jpg(folder_path: str) -> None:
    """
    Validate and convert HEIC files in the specified directory to JPG format.
    
    Args:
        folder_path (str): Path to the folder containing HEIC files
        
    Raises:
        ValueError: If the path doesn't exist or isn't a directory
    """
    # Convert string path to Path object for easier handling
    path = Path(folder_path)
    
    
    # Check if path exists
    if not path.exists():
        raise ValueError(f"The path {folder_path} does not exist")
        
    # Check if it's a directory
    if not path.is_dir():
        raise ValueError(f"The path {folder_path} is not a directory")
    
    # Get all HEIC files in the directory
    
    # test


if __name__ == "__main__":
    test_path = "/Volumes/T7/convert-from-heic"  
    try:
        convert_to_jpg(test_path)
    except ValueError as e:
        print(f"Error: {e}")