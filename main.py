import torch
import cv2
import numpy as np
import pathlib
import serial
import time
import keyboard  # Import keyboard module for key detection

pathlib.PosixPath = pathlib.WindowsPath

path = 'C:/Users/dtjab/anaconda3/envs/group3/best.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', path, force_reload=True)

cap = cv2.VideoCapture(0)

arduino_port = 'COM7'
arduino_baudrate = 9600
arduino = serial.Serial(arduino_port, arduino_baudrate, timeout=0)
time.sleep(0)

buzzer_activated = False  # Flag to track buzzer activation

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize input frame to smaller resolution
    frame = cv2.resize(frame, (640, 480))

    # Inference
    results = model(frame)

    # Extract detections
    boxes = results.xyxy[0]

    # Initialize flags
    Gloves = False
    Face_mask = False
    Goggles = False
    Labcoat = False

    # Process detections
    for box in boxes:
        label = int(box[5])
        if label == 0:
            Gloves = True
        elif label == 1:
            Labcoat = True
        elif label == 2:
            Face_mask = True
        elif label == 3:
            Goggles = True

    # Send commands to Arduino
    arduino.write(b'A' if Gloves else b'E')
    arduino.write(b'B' if Face_mask else b'E')
    arduino.write(b'C' if Goggles else b'E')
    arduino.write(b'D' if Labcoat else b'E')

    # Check if all objects are detected and buzzer not activated
    if Gloves and Face_mask and Goggles and Labcoat and not buzzer_activated:
        arduino.write(b'F')  # Send command to activate buzzer
        buzzer_activated = True
        print("All classes detected. Activating LEDs and buzzer.")

    # Display annotated frame
    annotated_frame = results.render()[0]
    cv2.imshow('YOLOv5 Detection', annotated_frame)

    # Check if 's' key is pressed for screen capture
    if keyboard.is_pressed('s'):
        cv2.imwrite('screencapture.jpg', annotated_frame)
        print("Screen capture saved as 'screencapture.jpg'.")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
