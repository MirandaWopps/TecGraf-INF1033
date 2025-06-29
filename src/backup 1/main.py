import cv2
import mediapipe as mp
import numpy as np
import csv
import matplotlib.pyplot as plt
from fpdf import FPDF


# ----- Função para calcular ângulo -----
def calcular_angulo(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cos_angulo = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angulo = np.degrees(np.arccos(np.clip(cos_angulo, -1.0, 1.0)))
    return angulo



# ----- Inicialização do MediaPipe -----
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# ----- Coleta dos dados -----
angulos_joelho = []
angulos_tornozelo = []

cap = cv2.VideoCapture('videoplayback.mp4')

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
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

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

# ----- Salvando os logs -----
with open('log_angulos.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Frame', 'Joelho', 'Tornozelo'])
    for i, (j, t) in enumerate(zip(angulos_joelho, angulos_tornozelo)):
        writer.writerow([i, j, t])


# ----- Função para análise robusta -----
def analise_robusta(nome, dados):
    dados_np = np.array(dados)
    mediana = np.median(dados_np)
    p25 = np.percentile(dados_np, 25)
    p75 = np.percentile(dados_np, 75)
    minimo = np.min(dados_np)
    maximo = np.max(dados_np)

    print(f'\n---- {nome} (Robusta) ----')
    print(f'Mediana: {mediana:.2f}')
    print(f'Percentil 25%: {p25:.2f}')
    print(f'Percentil 75%: {p75:.2f}')
    print(f'Mínimo: {minimo:.2f}')
    print(f'Máximo: {maximo:.2f}')
    print(f'IQR: [{p25:.2f}, {p75:.2f}]')

    return {
        "mediana": mediana,
        "p25": p25,
        "p75": p75,
        "minimo": minimo,
        "maximo": maximo
    }


# ----- Função para Bootstrap -----
def bootstrap_ic(dados, n_resamples=10000, confianca=95):
    dados = np.array(dados)
    medias = []

    for _ in range(n_resamples):
        amostra = np.random.choice(dados, size=len(dados), replace=True)
        medias.append(np.mean(amostra))

    lower = np.percentile(medias, (100 - confianca) / 2)
    upper = np.percentile(medias, 100 - (100 - confianca) / 2)

    return lower, upper


# ----- Execução das análises -----
result_joelho = analise_robusta("Joelho", angulos_joelho)
result_tornozelo = analise_robusta("Tornozelo", angulos_tornozelo)

ic_joelho = bootstrap_ic(angulos_joelho)
ic_tornozelo = bootstrap_ic(angulos_tornozelo)

print(f"IC Joelho (Bootstrap 95%): {ic_joelho}")
print(f"IC Tornozelo (Bootstrap 95%): {ic_tornozelo}")

# ----- Plotagem dos gráficos -----
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(angulos_joelho, label='Joelho')
plt.axhline(result_joelho['mediana'], color='red', linestyle='--', label='Mediana')
plt.title('Ângulo do Joelho')
plt.xlabel('Frame')
plt.ylabel('Ângulo (graus)')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(angulos_tornozelo, color='orange', label='Tornozelo')
plt.axhline(result_tornozelo['mediana'], color='red', linestyle='--', label='Mediana')
plt.title('Ângulo do Tornozelo')
plt.xlabel('Frame')
plt.ylabel('Ângulo (graus)')
plt.legend()

plt.tight_layout()
plt.savefig('grafico.png')
plt.show()

# ----- Relatório PDF -----
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(200, 10, 'Relatório de Análise de Ângulos', ln=True, align='C')

pdf.set_font('Arial', '', 12)
pdf.ln(10)

# Dados Joelho
pdf.cell(0, 10, f"Joelho - Mediana: {result_joelho['mediana']:.2f} | Max: {result_joelho['maximo']:.2f} | Min: {result_joelho['minimo']:.2f}", ln=True)
pdf.cell(0, 10, f"IQR (25%-75%): {result_joelho['p25']:.2f} - {result_joelho['p75']:.2f}", ln=True)
pdf.cell(0, 10, f"IC Bootstrap (95%): {ic_joelho[0]:.2f} - {ic_joelho[1]:.2f}", ln=True)

pdf.ln(5)

# Dados Tornozelo
pdf.cell(0, 10, f"Tornozelo - Mediana: {result_tornozelo['mediana']:.2f} | Max: {result_tornozelo['maximo']:.2f} | Min: {result_tornozelo['minimo']:.2f}", ln=True)
pdf.cell(0, 10, f"IQR (25%-75%): {result_tornozelo['p25']:.2f} - {result_tornozelo['p75']:.2f}", ln=True)
pdf.cell(0, 10, f"IC Bootstrap (95%): {ic_tornozelo[0]:.2f} - {ic_tornozelo[1]:.2f}", ln=True)

pdf.ln(10)
pdf.image('grafico.png', x=10, w=190)

pdf.output('relatorio_angulos.pdf')
