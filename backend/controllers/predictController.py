from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from torchvision import transforms
from PIL import Image
import torch
from fastapi import APIRouter
from torchvision import models, transforms
from fastapi import APIRouter, Depends
from models.usuario import UsuarioModel
from services.usersServices import getCurrentUser  # a

router = APIRouter()

# Carregando o modelo PyTorch já treinado (exemplo com .pth)
model = torch.load("weight/resnet_model_checkpoint.pth", map_location=torch.device("cpu"))

model = models.resnet50(pretrained=False)  # ou resnet50, conforme você treinou
num_classes = 2  # só duas classes
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

# 2️⃣ Carregar os pesos
state_dict = torch.load("weight/resnet_model_checkpoint.pth", map_location=torch.device("cpu"))
model.load_state_dict(state_dict)

# 3️⃣ Colocar o modelo em modo de avaliação
model.eval()



# Transformações da imagem (ajustar conforme seu modelo foi treinado)
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # redimensiona
    transforms.ToTensor(),          # converte para tensor
    transforms.Normalize(           # normaliza
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225]
    )
])

@router.post("/predict")
async def predict(file: UploadFile = File(...), current_user: UsuarioModel = Depends(getCurrentUser)  ):
    try:
        # Abre a imagem recebida
        image = Image.open(file.file).convert("RGB")
        image = transform(image).unsqueeze(0)  # adiciona batch dimension

        # Faz a previsão
        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs, 1)
            predicted_class = predicted.item()

        return JSONResponse(content={"classe_prevista": predicted_class})
    
    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)
