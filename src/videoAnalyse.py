# videoAnalyse.py
import cv2
import mediapipe as mp
import numpy as np

class VideoAnalyzer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.angulos_joelho, self.angulos_tornozelo = [], []
        self.cap = cv2.VideoCapture(self.video_path)
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.paused = False
        self.stopped = False

    def process_next_frame(self):
        if self.paused:
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            self.stopped = True
            return None

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark

            try:
                quadril = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                           landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                joelho = [landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                tornozelo = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                             landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                calcanhar = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
                             landmarks[self.mp_pose.PoseLandmark.RIGHT_HEEL.value].y]

                angulo_joelho = self.calcular_angulo(quadril, joelho, tornozelo)
                angulo_tornozelo = self.calcular_angulo(joelho, tornozelo, calcanhar)

                self.angulos_joelho.append(angulo_joelho)
                self.angulos_tornozelo.append(angulo_tornozelo)

                cv2.putText(frame, f'Joelho: {int(angulo_joelho)}', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f'Tornozelo: {int(angulo_tornozelo)}', (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            except:
                pass

        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def calcular_angulo(self, a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        ba, bc = a - b, c - b
        cos_angulo = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angulo = np.degrees(np.arccos(np.clip(cos_angulo, -1.0, 1.0)))
        return angulo

    def release(self):
        self.cap.release()
   


