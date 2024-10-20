import os
from dotenv import load_dotenv
from ultralytics import YOLO
import cv2
import time
import json
import boto3

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_DEFAULT_REGION')
AWS_S3_BUCKET_NAME=os.getenv('AWS_S3_BUCKET_NAME')



def upload_frame_to_s3(frame, bucket_name, frame_name):
    # Initialize S3 client
    s3_client = boto3.client(service_name='s3', region_name= AWS_REGION,
                             aws_access_key_id= AWS_ACCESS_KEY, aws_secret_access_key= AWS_SECRET_ACCESS_KEY)
    
    _, buffer = cv2.imencode('.jpg', frame)  # Encode the frame as JPEG
    s3_client.put_object(Bucket=bucket_name, Body=buffer.tobytes(), Key=frame_name)


# Initialize camera
cap = cv2.VideoCapture('Test Videos\Test 4.mp4')
cap.set(3, 1920)
cap.set(4, 1080)

# Load YOLOv8 model
model = YOLO("XDreamv1(m).pt")

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
                "Detection Zone ID": None,
                "Status": {
                    "LED": False,
                    "ULT": False,
                    "BDS": False
                }
            }
        }

        detected = False
        
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

                # Draw the bounding box and label on the image
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(img, f"{class_name} ({confidence:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)
            
                # # Determine the detection zone ID
                if x1 < 320:
                    detection_data["Alarm Message"]["Detection Zone ID"] = "A"
                else:
                    detection_data["Alarm Message"]["Detection Zone ID"] = "B"

                detected = True

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
                
        if detected:
            timestamp = int(time.time())
            frame_name = f"detection_{timestamp}.jpg"
            upload_frame_to_s3(img, 'boarbucket' , frame_name)
                
        # Display the resulting image
        cv2.imshow("YOLOv8 Prediction", img)

        # Update the last capture time
        last_capture_time = current_time

        # print(json.dumps(detection_data, indent=2))


    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
