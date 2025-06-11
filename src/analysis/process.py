import cv2

def process_frame(frame):
    """
    Aplica um processamento simples ao frame de vídeo.
    Neste exemplo, converte o frame para escala de cinza e desenha um texto.
    Você pode substituir essa lógica pela análise de pose, cálculo de ângulos, etc.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    cv2.putText(
        frame_processed,
        "Frame processado",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
        cv2.LINE_AA
    )

    return frame_processed
