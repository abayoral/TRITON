import os
from PIL import Image

def convert_png_to_jpg(png_file_path, jpg_file_path):
    try:
        # Open the PNG image
        with Image.open(png_file_path) as img:
            # Ensure the image is converted to RGB
            rgb_img = img.convert('RGB')
            # Save the image as a JPG file
            rgb_img.save(jpg_file_path, 'JPEG')
        print(f"Successfully converted {png_file_path} to {jpg_file_path}")
    except Exception as e:
        print(f"Error converting {png_file_path}: {e}")

def convert_and_delete_pngs_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            png_file_path = os.path.join(directory, filename)
            jpg_file_path = os.path.join(directory, filename.replace('.png', '.jpg'))
            convert_png_to_jpg(png_file_path, jpg_file_path)
            try:
                os.remove(png_file_path)
                print(f"Deleted {png_file_path}")
            except Exception as e:
                print(f"Error deleting {png_file_path}: {e}")

# Specify the directory containing PNG files
test_images_directory = 'sim_test_images'
convert_and_delete_pngs_in_directory(test_images_directory)
