import cv2
from ultralytics import YOLO
import uuid
import os
from moviepy.editor import VideoFileClip

def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def intersects_line(box, line):
    x1, y1, x2, y2 = box
    mid_x = int((x1 + x2) / 2)
    top_y = int(y1)
    bottom_y = int(y2)
    box_line = [(mid_x, top_y), (mid_x, bottom_y)]
    return intersect(line[0], line[1], box_line[0], box_line[1])

def run_yolo_tracking(video_source="your_video.mp4", model_path="yolov8m.pt", x1=0, y1=0, x2=0, y2=0):
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

    # Setup tracking + config
    results = model.track(
        source=video_source,
        conf=0.3,
        persist=True,
        stream=True,
        classes=[0],  # only person
        tracker="miawtracker.yaml"
    )

    # --- Garis vertikal dan variabel counting ---
    line = [(x1, y1), (x2, y2)]
    line_color = (0, 255, 255)
    count = 0
    track_history = {}

    frame_count = 0
    print("[INFO] Starting detection and tracking...")
    
    for r in results:
        frame = r.orig_img
        boxes = r.boxes
        frame_count += 1
        print(f"[INFO] Processing frame {frame_count}")

        # Gambar garis counting
        cv2.line(frame, line[0], line[1], line_color, 2)

        ids_in_frame = set()

        for box in boxes:
            if box.id is None:
                continue

            track_id = int(box.id[0])
            ids_in_frame.add(track_id)

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            if track_id not in track_history:
                track_history[track_id] = {"is_passing": False}

            if intersects_line((x1, y1, x2, y2), line) and not track_history[track_id]["is_passing"]:
                track_history[track_id]["is_passing"] = True
                count += 1
                print(f"[COUNT] Track ID {track_id} crossed the line. Total count: {count}")

            # Gambar box dan ID
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'ID:{track_id} {conf:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Hapus track_id yang sudah tidak muncul
        to_delete = [tid for tid in track_history if tid not in ids_in_frame]
        for tid in to_delete:
            del track_history[tid]

        # Tampilkan jumlah counting
        cv2.putText(frame, f'Count: {count}', (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        out.write(frame)
        cv2.imshow("Tracking", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

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