from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
import cv2
import numpy as np
import base64
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

app = FastAPI()

#modelos
modelo_parafusos = YOLO(
    os.getenv("PARAFUSO_MODEL", "pesos/best_parafuso.pt")
)

modelo_fissuras = YOLO(
    os.getenv("FISSURA_MODEL", "pesos/best_fissura.pt")
)

#função auxiliar
def executar_modelo(modelo, img, conf=0.5):

    results = modelo(img, conf=conf)

    annotated_img = results[0].plot()

    success, buffer = cv2.imencode(".jpg", annotated_img)

    if not success:
        return {
            "error": "image encoding failed"
        }

    img_base64 = base64.b64encode(buffer).decode("utf-8")

    detections = []

    for r in results:
        for b in r.boxes:

            classe_id = int(b.cls[0])

            detections.append({
                "classe": modelo.names[classe_id],
                "conf": float(b.conf[0]),
                "xyxy": b.xyxy.tolist()[0]
            })

    return {
        "count": len(detections),
        "detections": detections,
        "image": img_base64
    }

#endpoint parafusos
@app.post("/predict/parafusos")
async def predict_parafusos(file: UploadFile = File(...)):

    image_bytes = await file.read()

    np_arr = np.frombuffer(image_bytes, np.uint8)

    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    resultado = executar_modelo(
        modelo=modelo_parafusos,
        img=img,
        conf=0.5
    )

    return resultado

#endpoint fissuras
@app.post("/predict/fissuras")
async def predict_fissuras(file: UploadFile = File(...)):

    image_bytes = await file.read()

    np_arr = np.frombuffer(image_bytes, np.uint8)

    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    resultado = executar_modelo(
        modelo=modelo_fissuras,
        img=img,
        conf=0.5
    )

    return resultado