import torchvision.models as models 
import torch

class ImagemDetectionModels:

    def resnet50(num_class) -> models:
        # Create instace of resnet50
        model = models.resnet50(weights = "ResNet50_Weights.DEFAULT")
        # Take total features from the last layer
        num_features = model.fc.in_features
        # Create my own layer with num_class do i want
        model.fc = torch.nn.Linear(num_features, num_class)
        # Multi category cross entropy(Funcao de erro)
        # Binario e multi categorico
        return model
    
    def resnet101(num_class) -> models:
    # Create instace of resnet101
        model = models.resnet101(weights = "ResNet101_Weights.DEFAULT")
        # Take total features from the last layer
        num_features = model.fc.in_features
        # Create my own layer with num_class do i want
        model.fc = torch.nn.Linear(num_features, num_class)
        # Multi category cross entropy(Funcao de erro)
        # Binario e multi categorico
        return model    