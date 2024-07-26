import cv2
import os

def resize_images_in_place(folder_path, target_width=640, target_height=640):
    # Get all JPEG images in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)

        # Read and resize the image
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, (target_width, target_height))

        # Save the resized image (overwriting the original)
        cv2.imwrite(image_path, resized_image)
        print(f"Resized image saved: {image_path}")

if __name__ == "__main__":
    folder_path = "test_images"  # Change this to the path of your folder
    resize_images_in_place(folder_path)
