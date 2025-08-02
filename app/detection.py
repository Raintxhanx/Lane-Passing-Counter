import cv2
from ultralytics import YOLO
import uuid
import os
from moviepy.editor import VideoFileClip

def run_yolo_tracking(video_source="your_video.mp4", model_path="yolov11m.pt"):
    print(f"[INFO] Processing video: {video_source}")
    
    # Get video properties
    cap = cv2.VideoCapture(video_source)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()

    # Setup output video
    output_dir = os.path.dirname(video_source)
    out_path = os.path.join(output_dir, f"output_{uuid.uuid4().hex}.mp4")
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    print(f"[INFO] Loading YOLO model: {model_path}")
    model = YOLO(model_path)

    # Use simpler tracker configuration to avoid fuse_score error
    results = model.track(
        source=video_source,
        conf=0.3,
        persist=True,
        stream=True,
        classes=[0],  # only person
        tracker="bytetrack.yaml"
    )

    frame_count = 0
    print("[INFO] Starting detection and tracking...")
    
    for r in results:
        frame = r.orig_img
        boxes = r.boxes
        frame_count += 1
        print(f"[INFO] Processing frame {frame_count}")

        for box in boxes:
            track_id = int(box.id[0]) if box.id is not None else -1
            conf = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            color = (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f'ID:{track_id} {conf:.2f}', (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Save frame to video
        out.write(frame)
        
        # Display frame
        cv2.imshow("Tracking", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

    # Cleanup
    out.release()
    cv2.destroyAllWindows()
    
    print(f"[INFO] Processing completed!")
    print(f"[INFO] Total frames processed: {frame_count}")
    print(f"[INFO] Output saved to: {out_path}")
    
    # Convert to H.264 if necessary
    old_out_path = out_path
    out_path = convert_to_h264(out_path, out_path.replace('.mp4', '_h264.mp4'))
    os.remove(old_out_path)  # Remove old file if conversion was successful

    return out_path

def convert_to_h264(input_path, output_path):
    try:
        clip = VideoFileClip(input_path)
        clip.write_videofile(output_path, codec='libx264', preset='medium')
        return output_path
    except Exception as e:
        print(f"[ERROR] Conversion failed: {e}")
        return input_path