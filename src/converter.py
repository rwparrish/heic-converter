from pathlib import Path
from pillow_heif import register_heif_opener
from PIL import Image
from PIL.ExifTags import TAGS
from fractions import Fraction

register_heif_opener()


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
    image = Image.open(heic_files[0])
    get_gps_coordinates(image)
    # for file in heic_files:
    #     image = Image.open(file)
    #     image.save(file.with_suffix(".jpg"), "JPEG", quality=95)  # Quality ranges from 1 (worst) to 95 (best)
    #     print(f"Converted {file} to {file.with_suffix('.jpg')}")
       
    
def get_gps_coordinates(img: Image.Image) -> tuple[float, float] | None:
    """
    Extract GPS coordinates from an opened image.
    """
    try:
        exif = img.getexif()
        if exif is None:
            return None
            
        gps_info = exif.get_ifd(34853)
        if not gps_info:
            return None
            
        # Convert fractions to decimal degrees
        def convert_to_decimal(value):
            if isinstance(value, tuple):
                # Handle degree/minute/second format
                return value[0] + value[1]/60 + value[2]/3600
            elif isinstance(value, Fraction):
                # Handle Fraction objects
                return float(value)
            elif '/' in str(value):
                # Handle fraction strings
                num, denom = map(float, str(value).split('/'))
                return float(num/denom)
            return float(value)
            
        lat = convert_to_decimal(gps_info[2])
        if gps_info[1] == 'S': lat = -lat
            
        lon = convert_to_decimal(gps_info[4])
        if gps_info[3] == 'W': lon = -lon
        
        print(f"Decimal coordinates: {float(lat):.6f}, {float(lon):.6f}")
        return (lat, lon)
        
    except Exception as e:
        print(f"Error reading GPS data: {e}")
        return None
    

if __name__ == "__main__":
    test_path = "/Volumes/T7/convert-from-heic"
    try:
        convert_to_jpg(test_path)
    except ValueError as e:
        print(f"Error: {e}")
