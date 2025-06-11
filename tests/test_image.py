import cv2
import mediapipe as mp
import math

def compute_knee_angle(image_rgb) -> float:
    
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)    

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
        return angle

    else:
        return None
    

# TDD - Test Driven Development
def test_should_calculate_knee_angle():
    # Teste para verificar se o ângulo do joelho é calculado corretamente
    # Aqui você pode definir os pontos de teste e o ângulo esperado    
    # Inicializa o Mediapipe
   

    # Carrega a imagem
    image = cv2.imread('test_data/test_case_143.png')  # <- coloque o nome da imagem correta
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    angle = compute_knee_angle(image_rgb)

    assert angle is not None, "O ângulo do joelho não foi calculado."
    assert isinstance(angle, float), "O ângulo do joelho deve ser um número de ponto flutuante."

    tolerance_percent = 0.05
    expected_angle = 143
    tolerance = expected_angle * tolerance_percent
    assert abs(angle - expected_angle) <= tolerance, f"O ângulo do joelho ({angle}) não está dentro da tolerância de {tolerance_percent*100}% de {expected_angle}."