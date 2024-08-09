from ultralytics import YOLO
from serial import Serial
import cv2
import time
import json
import threading

# Load YOLOv8 model
model = YOLO("XDreamv1(n).pt")

# List of RTSP stream URLs
rtsp_urls = ['rtsp://admin:devgraphite2024@192.168.1.168:554/Streaming/Channels/101',
             'rtsp://admin:devgraphite2024@192.168.1.168:554/Streaming/Channels/201',
             'rtsp://admin:devgraphite2024@192.168.1.168:554/Streaming/Channels/301']

def process_stream(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    cap.set(3, 1280)
    cap.set(4, 720)

    # Set the capture interval in seconds
    capture_interval = 5
    last_capture_time = 0

    while True:
        # Read a frame from the camera
        success, img = cap.read()
        if not success:
            break

        # Check if it's time to capture a new frame
        current_time = time.time()
        if current_time - last_capture_time >= capture_interval:
            results = model(img)

            # Initialize the JSON data
            detection_data = {
                "Alarm Message": {
                    "Detection Zone ID": "A",
                    "Status": {
                        "LED": False,
                        "ULT": False,
                        "BDS": False
                    }
                }
            }

            # Iterate over the detected objects
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get the bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # Get the class name and confidence score
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    confidence = float(box.conf[0])

                    # Determine the detection zone ID
                    if x1 < 320:
                        detection_data["Alarm Message"]["Detection Zone ID"] = "A"
                    else:
                        detection_data["Alarm Message"]["Detection Zone ID"] = "B"

                    # Set the status flags based on the detected class
                    if class_name == "boar":
                        detection_data["Alarm Message"]["Status"]["LED"] = True
                        detection_data["Alarm Message"]["Status"]["ULT"] = True
                        detection_data["Alarm Message"]["Status"]["BDS"] = True
                    elif class_name == "dog":
                        detection_data["Alarm Message"]["Status"]["ULT"] = False
                        detection_data["Alarm Message"]["Status"]["ULT"] = False
                        detection_data["Alarm Message"]["Status"]["BDS"] = False
                    elif class_name == "cow":
                        detection_data["Alarm Message"]["Status"]["BDS"] = False
                        detection_data["Alarm Message"]["Status"]["ULT"] = False
                        detection_data["Alarm Message"]["Status"]["BDS"] = False
                    elif class_name == "person":
                        detection_data["Alarm Message"]["Status"]["LED"] = False
                        detection_data["Alarm Message"]["Status"]["ULT"] = False
                        detection_data["Alarm Message"]["Status"]["BDS"] = False

            # Update the last capture time
            last_capture_time = current_time

            uart = Serial(port='/dev/ttyTHS0', baudrate=115200, timeout=1)
            json_message = json.dumps(detection_data)
            print(f"Detection in stream: {rtsp_url}")
            print(json_message)
            uart.write(json_message.encode())
            uart.close()

    cap.release()

# Create a thread for each RTSP stream
threads = []
for rtsp_url in rtsp_urls:
    t = threading.Thread(target=process_stream, args=(rtsp_url,))
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()
