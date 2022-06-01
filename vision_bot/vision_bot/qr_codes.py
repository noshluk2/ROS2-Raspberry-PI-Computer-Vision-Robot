import cv2

# img = cv2.imread('input_qrr.png')
import numpy as np
cap = cv2.VideoCapture('qr_codes.avi')

decoder = cv2.QRCodeDetector()
while True:
    _, frame = cap.read()
    data, points, _ = decoder.detectAndDecode(frame)


    if points is not None:
        print('Decoded data: ' + data)

        points = points[0]
        for i in range(len(points)):
            pt1 = [int(val) for val in points[i]]
            pt2 = [int(val) for val in points[(i + 1) % 4]]
            cv2.line(frame, pt1, pt2, color=(255, 0, 0), thickness=3)

    cv2.imshow('Detected QR code', frame)
    cv2.waitKey(10)
    cv2.destroyAllWindows()