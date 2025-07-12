# videoAnalyse.py
import cv2
import mediapipe as mp
import numpy as np

class VideoAnalyzer: #Class to analyze video and calculate angles of knee and ankle

#TODO: algo tem de ser feito para se o video pathing nao for de fato um video lançar uma exceção !

    def __init__(self, video_path): #params 1 (nothing, video path)| ALREADY STARTS WITH A FUNCTION
        # Error Treatment 1: Garantee that the video path is a video file.
        valid_extensions = ('mp4', 'wmv', 'avi', 'mov', 'avchd', 'flv', 'f4v', 'swf', 'mkv', 'webm') #valid video formats
        file_extension = video_path.lower().split('.')[-1]#solving up case possibility + catching the extension
        if file_extension not in valid_extensions: # is the extension not in the list ?
            raise ValueError(f"Invalid video format. Supported formats: {valid_extensions}")#so, show error        

        self.video_path = video_path #arg video_path
        self.angulos_joelho, self.angulos_tornozelo = [], []# vectors to store angles
        self.cap = cv2.VideoCapture(self.video_path)#starts video capture        
        if not self.cap.isOpened(): # Additional check if video opened successfully
            raise IOError("Could not open video file. The file might be corrupted or the codec is not supported.")


        self.mp_pose = mp.solutions.pose #Acessing module mediapipe.pose and saving reference in self.mp_pose, the class atribute
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.stopped = False #Controls when video ends.

    def process_next_frame(self): #params 1 (nothing)
        ret, frame = self.cap.read()#returns (avaliability of video,frame)
        if not ret: #if ret ==0 it means no frame was read
            self.stopped = True #flag video ended
            return None #no return needed

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark

            try:#Attempt to calculate angles
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
            except:#Exception treatment
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