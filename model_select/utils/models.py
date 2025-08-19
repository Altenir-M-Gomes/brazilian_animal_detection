import torchvision.models as models 
import torch
from ultralytics import YOLO


class ImagemDetectionModels:

    @staticmethod
    def resnet50(num_class: int = 2) -> models:
        # Create instace of resnet50
        model = models.resnet50(weights = "ResNet50_Weights.DEFAULT")
        # Take total features from the last layer
        num_features = model.fc.in_features
        # Create my own layer with num_class do i want
        model.fc = torch.nn.Linear(num_features, num_class)
        # Multi category cross entropy(Funcao de erro)
        # Binario e multi categorico
        return model
    
    @staticmethod
    def resnet101(num_class: int = 2) -> torch.nn.Module:
        model = models.resnet101(weights=models.ResNet101_Weights.DEFAULT)
        num_features = model.fc.in_features
        model.fc = torch.nn.Linear(num_features, num_class)
        return model

    @staticmethod
    def vgg16(num_class: int = 2) -> torch.nn.Module:
        model = models.vgg16(weights=models.VGG16_Weights.DEFAULT)
        num_features = model.classifier[6].in_features
        # substitui a última camada (fc)
        model.classifier[6] = torch.nn.Linear(num_features, num_class)
        return model

    @staticmethod
    def vgg16_bn(num_class: int = 2) -> torch.nn.Module:
        model = models.vgg16_bn(weights=models.VGG16_BN_Weights.DEFAULT)
        num_features = model.classifier[6].in_features
        # substitui a última camada (fc)
        model.classifier[6] = torch.nn.Linear(num_features, num_class)
        return model

    @staticmethod
    def yolov8(model_name: str = "yolov8n", num_class: int = 2):
        """
        model_name pode ser: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
        """
        model = YOLO(model_name + ".pt")  # carrega pesos pré-treinados
        if num_class:
            # reconfigura a cabeça de predição
            model.model.model[-1] = torch.nn.Conv2d(
                in_channels=model.model.model[-1].in_channels,
                out_channels=num_class * (model.model.model[-1].out_channels // model.model.model[-1].in_channels),
                kernel_size=1
            )
        return model
