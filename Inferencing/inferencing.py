from ultralytics import YOLO
import cv2
import time

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Load YOLOv8 model
model = YOLO("PATH to .pt file of your model")

# Set the capture interval in seconds
capture_interval = 0

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

        # Display the resulting image
        cv2.imshow("YOLOv8 Prediction", img)

        # Update the last capture time
        last_capture_time = current_time

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
