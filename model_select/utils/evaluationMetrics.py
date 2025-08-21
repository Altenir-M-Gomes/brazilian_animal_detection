import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader
import torch
from typing import Tuple
import numpy as np
from .evalutaionDataClass import EvaluationDataClass
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)



class Metrics:
    def __init__(self, model: nn.Module, device: torch.device, test_data: DataLoader, outPutDim: int = 2):
        self.originalModel = model
        self.model = model.eval()
        self.device = device
        self.data = test_data
        self.outPutDim = outPutDim
        self.y_pred = np.zeros(0, dtype=int)
        self.y_true = np.zeros(0, dtype=int)
        self.y_score = np.zeros(0, dtype=int)
        
    def trainTestData(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        self.model.eval()  # garante que usamos o modelo atualizado em modo eval
        y_pred = np.zeros(0, dtype=int)
        y_true = np.zeros(0, dtype=int)
        y_score = np.empty((0, self.outPutDim))

        with torch.no_grad():
            for images_batch, labels_batch in self.data:
                images_batch = images_batch.to(self.device)

                scores = self.model(images_batch)
                _, y_pred_batch = scores.max(1)

                y_pred_batch = y_pred_batch.cpu().numpy()
                labels_batch = labels_batch.numpy()
                y_score_batch = torch.softmax(scores, dim=1).cpu().numpy()

                y_pred = np.concatenate((y_pred, y_pred_batch))
                y_true = np.concatenate((y_true, labels_batch))
                y_score = np.concatenate((y_score, y_score_batch))

        self.y_pred = y_pred
        self.y_true = y_true
        self.y_score = y_score
        return y_pred, y_true, y_score

            
    def getAccuracy(self) -> float:
        '''
            Evaluate the model's performance on the test data and print a classification report.

            Arguments:
            - test_data: a DataLoader containing the test dataset.
            - model: the trained model to evaluate.
        '''
        return accuracy_score(self.y_true, self.y_pred)

    def getPrecision(self) -> float:
        return precision_score(self.y_true, self.y_pred, average='weighted', zero_division=0)

    def getRecall(self) -> float:
        return recall_score(self.y_true, self.y_pred, average='weighted', zero_division=0)

    def getF1Score(self) -> float:
        return f1_score(self.y_true, self.y_pred, average='weighted', zero_division=0)
    
    def getConfusionMatrix(self) -> np.ndarray:
        return confusion_matrix(self.y_true, self.y_pred)

    def getAuroc(self) -> float:
        
        try:
            return roc_auc_score(self.y_true, self.y_score, multi_class='ovr', average='weighted')
        except ValueError:
            return 0.0
    def classificationReport(self) -> str | dict:
        return classification_report(self.y_true, self.y_pred)
    
    def colectMetrics(self) -> EvaluationDataClass:
        y_pred, y_true, y_score = self.trainTestData()

        return EvaluationDataClass(
            accuracy=self.getAccuracy(), 
            classification_report=self.classificationReport(),
            precision=self.getPrecision(),
            auroc=self.getAuroc(),  
            confusion_matrix=self.getConfusionMatrix(), 
            f1_score=self.getF1Score(), 
            recall=self.getRecall(),
            y_pred=y_pred, 
            y_score=y_score,
            y_true=y_true 
            )
