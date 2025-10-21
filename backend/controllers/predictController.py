from fastapi import APIRouter, UploadFile, File, Depends, status
from fastapi.responses import JSONResponse
from torchvision import transforms, models
from PIL import Image
import torch
from models.usuario import UsuarioModel
from services.usersServices import UserService
from ultils.wrapperExecption import wrap_exception

class PredictionController:
    router = APIRouter()

    # 1️⃣ Configuração do modelo
    model = models.resnet50(pretrained=False)
    num_classes = 2
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

    # Carrega pesos
    state_dict = torch.load("weight/resnet_model_checkpoint.pth", map_location=torch.device("cpu"))
    model.load_state_dict(state_dict)
    model.eval()  # modo avaliação

    # Transformações
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406], 
            std=[0.229, 0.224, 0.225]
        )
    ])

    @router.post("", status_code=status.HTTP_200_OK, tags=["Previsão"])
    @wrap_exception
    async def predict(file: UploadFile = File(...), current_user: UsuarioModel = Depends(UserService.getCurrentUser)):
        """
        Recebe uma imagem, aplica transformações e retorna a classe prevista pelo modelo.
        """
        # Abre a imagem e aplica transformações
        image = Image.open(file.file).convert("RGB")
        image = PredictionController.transform(image).unsqueeze(0)  # adiciona batch dimension

        # Faz a predição
        with torch.no_grad():
            outputs = PredictionController.model(image)
            _, predicted = torch.max(outputs, 1)
            predicted_class = predicted.item()

        return {"classe_prevista": predicted_class}
