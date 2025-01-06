import json
import os
from fastapi import UploadFile, File
from PIL import Image
import io
from fastapi.responses import JSONResponse
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import efficientnet_b0
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

model_name = "efficientnet_b0_identification_best.pth"
model_path = os.path.join(os.getenv('PATH_TO_MODELS'), model_name)

model = efficientnet_b0(pretrained=False)
# Ajuster la dernière couche pour 64 classes (ou votre nombre exact de classes)
num_classes = 64  # Remplacez par votre nombre de classes
model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

state_dict = torch.load(model_path, map_location=torch.device('cpu'))
model.load_state_dict(state_dict)  # Charger les poids
model.eval()  # Mettre le modèle en mode évaluation

# Define the image transformations
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

class ScanEspeceService():

    async def predict(file: UploadFile = File(...)):
        try:
            # Charger l'image
            image = Image.open(io.BytesIO(await file.read()))
            # image = Image.open(io.BytesIO(await file.read())).convert("RGB")

            # Appliquer les transformations
            input_tensor = transform(image).unsqueeze(0)  # Ajouter une dimension batch

            # Passer l'image dans le modèle
            with torch.no_grad():
                output = model(input_tensor)
                _, predicted = torch.max(output, 1)

            # Read file
            utilisateurs_json_file_path = os.path.join("app/enum", "espece_classes.json")
            with open(utilisateurs_json_file_path, "r") as file:
                especes_classes = json.load(file)

            prediction = especes_classes[predicted.item()]
            return {"prediction": prediction}
        
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)