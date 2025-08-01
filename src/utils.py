def load_model(model_path):
    # Function to load the YOLOv5 model
    import torch
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
    return model

def process_frame(frame, model):
    # Function to process a single frame for object detection
    results = model(frame)
    return results

def detect_objects(results):
    # Function to extract detected objects from the results
    detections = results.xyxy[0]  # Get detections in xyxy format
    return detections.tolist()  # Convert to list for easier handling