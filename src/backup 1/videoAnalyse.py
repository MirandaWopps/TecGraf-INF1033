import cv2
import mediapipe as mp
import numpy as np
import csv
import tkinter as tk
from tkinter import filedialog
import sys

from generierenGraphen import gerar_grafico
from generierenPDF import gerar_pdf

# Função para calcular o ângulo entre 3 pontos
def calcular_angulo(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cos_angulo = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angulo = np.degrees(np.arccos(np.clip(cos_angulo, -1.0, 1.0)))
    return angulo

# Inicialização do MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Listas para armazenar os ângulos
angulos_joelho = []
angulos_tornozelo = []

# Leitura do vídeo
if len(sys.argv) > 1:
    video_path = sys.argv[1]
else:
    video_path = 'videoplayback.mp4'

cap = cv2.VideoCapture(video_path)

# Processamento do vídeo frame a frame
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark

            try:
                quadril = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                joelho = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                tornozelo = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                calcanhar = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]

                angulo_joelho = calcular_angulo(quadril, joelho, tornozelo)
                angulo_tornozelo = calcular_angulo(joelho, tornozelo, calcanhar)

                angulos_joelho.append(angulo_joelho)
                angulos_tornozelo.append(angulo_tornozelo)

                cv2.putText(image, f'Joelho: {int(angulo_joelho)}',
                            (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(image, f'Tornozelo: {int(angulo_tornozelo)}',
                            (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            except:
                pass

        cv2.imshow('Pose Detection', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()



#Graphen
valores = gerar_grafico(angulos_joelho, angulos_tornozelo)

#PDF
gerar_pdf(valores)
