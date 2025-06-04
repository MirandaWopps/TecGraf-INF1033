import cv2
import mediapipe as mp
import math

# Inicializa o Mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)
mp_drawing = mp.solutions.drawing_utils

# Carrega a imagem
image = cv2.imread('test_data/test_case_143.png')  # <- coloque o nome da imagem correta
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Processa a imagem
results = pose.process(image_rgb)

if results.pose_landmarks:
    landmarks = results.pose_landmarks.landmark

    # Pega os pontos: quadril, joelho e tornozelo direito
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]


    def calculate_angle(a, b, c):
        a = [a.x, a.y]
        b = [b.x, b.y]
        c = [c.x, c.y]

        ba = [a[0] - b[0], a[1] - b[1]]
        bc = [c[0] - b[0], c[1] - b[1]]

        cosine_angle = (ba[0]*bc[0] + ba[1]*bc[1]) / (
            math.sqrt(ba[0]**2 + ba[1]**2) * math.sqrt(bc[0]**2 + bc[1]**2)
        )
        angle = math.degrees(math.acos(cosine_angle))
        return angle

    angle = calculate_angle(hip, knee, ankle)
    print(f"Ângulo do joelho direito: {angle:.2f} graus")

    # Desenha a pose
    annotated_image = image.copy()
    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS
    )

    # Mostra a imagem com os pontos
    while True:
        cv2.imshow('Pose', annotated_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

else:
    print("Nenhum corpo detectado na imagem.")
