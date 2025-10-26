import cv2
import matplotlib.pyplot as plt
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to open the camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Laplacian
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    # Convert the Laplacian image to an integer-valued image
    laplacian_abs = cv2.convertScaleAbs(laplacian)

    # Apply median filter to the Laplacian image
    median = cv2.medianBlur(laplacian_abs, 5)

    # Apply Canny edge detection
    edges = cv2.Canny(gray, 0, 100)

    plt.clf()

    plt.subplot(231)
    plt.imshow(gray, cmap='gray')
    plt.title('Grayscale')
    plt.axis("off")

    plt.subplot(232)
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.title('RGB')
    plt.axis("off")

    plt.subplot(233)
    plt.imshow(median, cmap='gray')
    plt.title('Laplacian with Median Filter')
    plt.axis("off")

    plt.subplot(234)
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.title('Original')
    plt.axis("off")

    plt.subplot(235)
    plt.imshow(edges, cmap='gray')
    plt.title('Canny Edge Detection')
    plt.axis("off")

    plt.tight_layout()
    plt.pause(0.1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything if the job is finished
cap.release()
cv2.destroyAllWindows()
