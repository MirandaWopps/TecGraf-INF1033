import cv2
import mediapipe as mp
import numpy as np
import csv
import matplotlib.pyplot as plt
from fpdf import FPDF
import sys

def calcular_angulo(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cos_angulo = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angulo = np.degrees(np.arccos(np.clip(cos_angulo, -1.0, 1.0)))
    return angulo

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

angulos_joelho = []
angulos_tornozelo = []

if len(sys.argv) > 1:
    video_path = sys.argv[1]
else:
    video_path = 'videoplayback.mp4'

cap = cv2.VideoCapture(video_path)

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

# Calcular os mínimos e máximos
min_joelho, max_joelho = np.min(angulos_joelho), np.max(angulos_joelho)
min_tornozelo, max_tornozelo = np.min(angulos_tornozelo), np.max(angulos_tornozelo)

print(f"\nJoelho - Min: {min_joelho:.2f}, Max: {max_joelho:.2f}")
print(f"Tornozelo - Min: {min_tornozelo:.2f}, Max: {max_tornozelo:.2f}")

# Plot com 2 linhas por gráfico:
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(angulos_joelho, label='Joelho')
plt.axhline(min_joelho, color='blue', linestyle='--', label='Mínimo')
plt.axhline(max_joelho, color='red', linestyle='--', label='Máximo')
plt.title('Ângulo do Joelho')
plt.xlabel('Frame')
plt.ylabel('Ângulo (graus)')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(angulos_tornozelo, color='orange', label='Tornozelo')
plt.axhline(min_tornozelo, color='blue', linestyle='--', label='Mínimo')
plt.axhline(max_tornozelo, color='red', linestyle='--', label='Máximo')
plt.title('Ângulo do Tornozelo')
plt.xlabel('Frame')
plt.ylabel('Ângulo (graus)')
plt.legend()

plt.tight_layout()
plt.savefig('grafico.png')
plt.show()

# PDF com os mesmos valores
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(200, 10, 'Relatório de Análise de Ângulos', ln=True, align='C')
pdf.set_font('Arial', '', 12)
pdf.ln(10)

pdf.cell(0, 10, f"Joelho - Min: {min_joelho:.2f} | Max: {max_joelho:.2f}", ln=True)
pdf.cell(0, 10, f"Tornozelo - Min: {min_tornozelo:.2f} | Max: {max_tornozelo:.2f}", ln=True)

pdf.ln(10)
pdf.image('grafico.png', x=10, w=190)

pdf.output('relatorio_angulos.pdf')

