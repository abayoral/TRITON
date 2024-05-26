import torch
import cv2
import os

def load_custom_model(model_path):
    """
    Load the custom-trained YOLOv5 model.
    :param model_path: The path to the custom-trained YOLOv5 model weights.
    :return: The loaded YOLOv5 model.
    """
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
    return model

def initialize_tracker():
    """
    Initialize an OpenCV CSRT tracker.
    :return: The initialized tracker.
    """
    tracker = cv2.TrackerCSRT_create()
    return tracker

def process_video(video_path, output_path, model):
    """
    Process the video to detect and track objects.
    :param video_path: The path to the input video file.
    :param output_path: The path to save the processed output video file.
    :param model: The loaded YOLOv5 model.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

    trackers = []
    tracker_initialized = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if not tracker_initialized:
            # Perform object detection
            results = model(frame)
            detections = results.pandas().xyxy[0]

            for _, row in detections.iterrows():
                x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
                bbox = (x1, y1, x2 - x1, y2 - y1)
                tracker = initialize_tracker()
                tracker.init(frame, bbox)
                trackers.append(tracker)
            
            tracker_initialized = True

        # Update all trackers
        for i, tracker in enumerate(trackers):
            success, bbox = tracker.update(frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f'Object {i}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                # Optionally, handle lost trackers here
                pass

        out.write(frame)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    model_path = 'yolov5/yolov5m.pt'  # Path to your custom-trained YOLOv5 model weights
    video_path = 'video/shaky.mp4' # Input video file path
    video_filename = os.path.basename(video_path)
    output_directory = 'processed_video'  # Output directory
    output_path = os.path.join(output_directory, video_filename)

    model = load_custom_model(model_path)  # Load custom YOLOv5 model
    process_video(video_path, output_path, model)

