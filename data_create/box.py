import cv2
import os

# Global variables
image = None
original_image = None
bounding_boxes = []
start_point = None
drawing = False
current_class = 0
colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]  # Colors for different classes
target_width = 640
target_height = 640

# Mouse callback function to draw bounding boxes
def draw_bounding_box(event, x, y, flags, param):
    global image, start_point, drawing, bounding_boxes, current_class

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = image.copy()
            cv2.rectangle(img_copy, start_point, (x, y), colors[current_class], 2)
            cv2.imshow('Image', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        bounding_boxes.append((start_point, end_point, current_class))
        cv2.rectangle(image, start_point, end_point, colors[current_class], 2)
        cv2.imshow('Image', image)

def save_annotations(image_path, bounding_boxes):
    height, width, _ = image.shape
    labels_dir = os.path.join(os.path.dirname(image_path), 'labels')
    os.makedirs(labels_dir, exist_ok=True)
    annotation_file = os.path.join(labels_dir, os.path.basename(image_path).replace('.jpg', '.txt'))

    with open(annotation_file, 'w') as file:
        for box in bounding_boxes:
            (x1, y1), (x2, y2), class_label = box
            center_x = (x1 + x2) / 2 / width
            center_y = (y1 + y2) / 2 / height
            bbox_width = (x2 - x1) / width
            bbox_height = (y2 - y1) / height
            file.write(f"{class_label} {center_x} {center_y} {bbox_width} {bbox_height}\n")

def process_image(image_path):
    global image, original_image, bounding_boxes, current_class
    image = cv2.imread(image_path)
    image = cv2.resize(image, (target_width, target_height))
    original_image = image.copy()
    bounding_boxes = []
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', draw_bounding_box)

    while True:
        img_copy = image.copy()
        cv2.putText(img_copy, f"Current class: {current_class} (Press '1', '2', '3' to change)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img_copy, "Press 's' to save, 'n' for next, 'u' to undo, 'q' to quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Image', img_copy)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            return False
        elif key == ord('s'):
            save_annotations(image_path, bounding_boxes)
            print(f"Annotations saved for {image_path}.")
        elif key == ord('n'):
            save_annotations(image_path, bounding_boxes)
            print(f"Annotations saved for {image_path}.")
            break
        elif key == ord('u'):
            if bounding_boxes:
                bounding_boxes.pop()
                image = original_image.copy()
                for box in bounding_boxes:
                    (x1, y1), (x2, y2), class_label = box
                    cv2.rectangle(image, (x1, y1), (x2, y2), colors[class_label], 2)
                print("Last bounding box undone.")
        elif key == ord('1'):
            current_class = 0
        elif key == ord('2'):
            current_class = 1
        elif key == ord('3'):
            current_class = 2

    cv2.destroyAllWindows()
    return True

def main(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f"Processing {image_path}")
        if not process_image(image_path):
            break

if __name__ == "__main__":
    folder_path = "sim_test_images"  # Change this to the path of your folder
    main(folder_path)
