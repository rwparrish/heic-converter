from pathlib import Path
from pillow_heif import register_heif_opener
from PIL import Image
from PIL.ExifTags import TAGS

# Register HEIF opener with Pillow
register_heif_opener()

def print_exif_data(dir_path):
    #create list of images
    images = [image for image in Path(dir_path).glob("*.HEIC")]
    """Helper function to print EXIF data in a readable format"""
    for image in images:
        with Image.open(image) as img:
            exif_data = img.getexif()
            if exif_data is None:
                print("No EXIF data found")
                return
                
            print("\nEXIF data:")
            for tag_id in exif_data:
                tag = TAGS.get(tag_id, tag_id)
                data = exif_data.get(tag_id)
                if isinstance(data, bytes):
                    data = data.decode()
                print(f"{tag}: {data}")

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
    heic_files = list(path.glob("*.HEIC")) + list(path.glob("*.heic"))
    
    if heic_files:
        # Let's examine EXIF data from the first file
        print_exif_data(heic_files[0])
        
    breakpoint()


if __name__ == "__main__":
    test_path = "/Volumes/T7/convert-from-heic"  
    try:
        print_exif_data(test_path)
        convert_to_jpg(test_path)
    except ValueError as e:
        print(f"Error: {e}")