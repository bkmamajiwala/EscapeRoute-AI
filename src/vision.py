import cv2
import numpy as np

class ObstacleDetector:
    def __init__(self, video_source=0):
        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)

    def detect_obstacles(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Fire detection (simple color detection)
            fire_mask = cv2.inRange(frame, (0, 0, 200), (100, 100, 255))
            fire_contours, _ = cv2.findContours(fire_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Smoke detection (simple color detection)
            smoke_mask = cv2.inRange(frame, (100, 100, 100), (200, 200, 200))
            smoke_contours, _ = cv2.findContours(smoke_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Draw contours for fire
            for contour in fire_contours:
                cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)  # Red for fire

            # Draw contours for smoke
            for contour in smoke_contours:
                cv2.drawContours(frame, [contour], -1, (255, 255, 0), 2)  # Blue for smoke

            cv2.imshow('Obstacle Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = ObstacleDetector()
    detector.detect_obstacles()