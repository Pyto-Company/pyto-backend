import json
import os
from typing import Dict, List
from fastapi import UploadFile, File
from PIL import Image, ImageFile
import io
from fastapi.responses import JSONResponse
from torchvision import transforms
import torch
from torchvision.models import efficientnet_b0
import torch.nn as nn

model = efficientnet_b0(pretrained=False)

num_classes = 17  # Remplacez par votre nombre de classes
model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

model_path = "././ai_models/efficientnet_b0_disease_best.pth"
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

class ScanMaladieService():

    def predict_common(self, image: ImageFile):
        # Appliquer les transformations
        input_tensor = transform(image).unsqueeze(0)  # Ajouter une dimension batch

        # Passer l'image dans le modèle
        with torch.no_grad():
            output = model(input_tensor)

        return output

    
    async def predict_higher(self,file: UploadFile = File(...)):
        try:
            # Charger l'image
            image = Image.open(io.BytesIO(await file.read()))
            # image = Image.open(io.BytesIO(await file.read())).convert("RGB")

            output = self.predict_common(image)
            _, predicted = torch.max(output, 1)

            # Read file
            utilisateurs_json_file_path = os.path.join("app/enum", "maladie_classes.json")
            with open(utilisateurs_json_file_path, "r") as file:
                especes_classes = json.load(file)

            prediction = especes_classes[predicted.item()]
            return {"prediction": prediction}
        
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)
    
    
    async def predict_all(self,file: UploadFile = File(...)) -> List[Dict[str, float]]:
        try:
            # Charger l'image
            image = Image.open(io.BytesIO(await file.read()))
            # image = Image.open(io.BytesIO(await file.read())).convert("RGB")

            output = self.predict_common(image)
            output_list = output.squeeze(0).tolist()

            # Read file
            utilisateurs_json_file_path = os.path.join("app/enum", "maladie_classes.json")
            with open(utilisateurs_json_file_path, "r") as file:
                especes_classes = json.load(file)

            # Create a list of dictionaries, where each dictionary contains disease and prediction
            predictions = [{"disease": especes_classes[i], "prediction": output_list[i]} for i in range(len(especes_classes))]

            return {"predictions": predictions}
        
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)
        
