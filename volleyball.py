import cv2
import numpy as np

cap = cv2.VideoCapture('/home/praket/projects/tda/openCV/volleyball_match.mp4') 
ball_trajectory = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow) # each pixel either black/white

    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) # removes small specks of noise
    mask = cv2.dilate(mask, kernel, iterations=1) # fills gaps in broken contours

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 100 < area < 800:  # small ball sized area

            # check circularity
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * (area / (perimeter * perimeter))

            if 0.6 < circularity < 1.2:
                (x, y, w, h) = cv2.boundingRect(cnt)
                cx, cy = x + w // 2, y + h // 2
                ball_trajectory.append((cx, cy))

                cv2.circle(frame, (cx, cy), 8, (0, 255, 255), -1)
                break  

    # draw ball trajectory
    for i in range(1, len(ball_trajectory)):
        cv2.line(frame, ball_trajectory[i - 1], ball_trajectory[i], (0, 0, 255), 2)

    cv2.imshow("Volleyball Tracker", frame)
    if cv2.waitKey(25) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
