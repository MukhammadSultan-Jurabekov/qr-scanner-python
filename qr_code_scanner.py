import cv2
from pyzbar import pyzbar

def scan_qr_code():
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Find QR codes in the frame
        decoded_objects = pyzbar.decode(frame)

        # Draw bounding box and display decoded text for each detected QR code
        for obj in decoded_objects:
            points = obj.polygon

            if len(points) > 4:  # If the points form a complex polygon, use convex hull
                hull = cv2.convexHull(points)
                points = hull.reshape(-1, 2)

            # Draw the bounding box
            for i in range(len(points)):
                cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % len(points)]), (0, 255, 0), 3)

            # Decode the QR code
            qr_data = obj.data.decode("utf-8")
            qr_type = obj.type

            # Put the decoded text on the image
            cv2.putText(frame, f'{qr_data} ({qr_type})', (points[0][0], points[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Display the resulting frame
        cv2.imshow('QR Code Scanner', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_qr_code()
