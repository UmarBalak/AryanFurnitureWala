from fastapi import FastAPI, File, UploadFile
from PIL import Image
import numpy as np
import os
import random
from furniture2 import detect_furniture, get_top_complementary_items, get_random_product_image

app = FastAPI()

# Load the YOLO model outside of the endpoint function to initialize it only once
from ultralytics import YOLO
model = YOLO('yolov9s.pt')

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(file.file)
    image = image.resize((640, 480))

    # Detect furniture
    detected_furniture = detect_furniture(image)

    if detected_furniture:
        # Generate complementary items
        top_complementary_furniture = get_top_complementary_items(detected_furniture)
        return {"detected_furniture": detected_furniture, "top_complementary_furniture": top_complementary_furniture}
    else:
        return {"detected_furniture": [], "top_complementary_furniture": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
