import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader
import torch
from typing import Tuple
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from functools import wraps
import numpy as np
from matplotlib.figure import Figure


class Metrics:

    def erroWrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"[WARNING] {func.__name__} falhou: {e}")
                return None
        return inner

    
    def __init__(self, model: nn.Module, device: torch.device, testDate: DataLoader, outPutDim: int = 2):
        # TODO: criar um style global para as figs

        self.model = model
        self.device = device
        self.data = testDate
        self.outPutDim = outPutDim
        
        yPred, yTrue, yScore = self._trainTestData()

        self.yTrue = yTrue
        self.yPred = yPred
        self.yScore = yScore

    def _trainTestData(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        yPred = np.zeros(0, dtype=int)
        yTrue = np.zeros(0, dtype=int)
        yScore = np.empty((0, self.outPutDim))

        self.model.eval()  
        with torch.no_grad():
            for images_batch, labels_batch in self.data:
                images_batch = images_batch.to(self.device)

                scores = self.model(images_batch)
                _, yPredBatch = scores.max(1)

                yPredBatch = yPredBatch.cpu().numpy()
                labels_batch = labels_batch.numpy()
                yScoreBatch = torch.softmax(scores, dim=1).cpu().numpy()

                yPred = np.concatenate((yPred, yPredBatch))
                yTrue = np.concatenate((yTrue, labels_batch))
                yScore = np.concatenate((yScore, yScoreBatch))

        return yPred, yTrue, yScore

    @erroWrapper       
    def _getAccuracy(self) -> float:
        return accuracy_score(self.y_true, self.y_pred)
    
    @erroWrapper       

    def _getPrecision(self) -> float:
        return precision_score(self.y_true, self.y_pred, average='weighted', zero_division=0)
    
    @erroWrapper       
    def _getRecall(self) -> float:
        return recall_score(self.y_true, self.y_pred, average='weighted', zero_division=0)
    
    @erroWrapper       
    def _getF1Score(self) -> float:
        return f1_score(self.y_true, self.y_pred, average='weighted', zero_division=0)
    
    @erroWrapper       
    def _getConfusionMatrix(self) -> np.ndarray:
        return confusion_matrix(self.y_true, self.y_pred)
    
    @erroWrapper       
    def _getAuroc(self) -> float:
        return roc_auc_score(self.y_true, self.y_score, multi_class='ovr', average='weighted')
    
    @erroWrapper       
    def _classificationReport(self) -> str | dict:
        return classification_report(self.y_true, self.y_pred)
    
    def __str__(self) -> str:
        self._trainTestData()

        return (
            f"📊 Evaluation Results\n"
            f"---------------------------\n"
            f"Accuracy:   {self._getAccuracy():.4f}\n"
            f"Precision:  {self._getPrecision():.4f}\n"
            f"Recall:     {self._getRecall():.4f}\n"
            f"F1 Score:   {self._getF1Score():.4f}\n"
            f"AUROC:      {self._getAuroc():.4f}\n\n"
            f"Confusion Matrix:\n{self._getConfusionMatrix()}\n\n"
            f"Classification Report:\n{self._classificationReport()}\n"
        )

    # TODO: retornar as figuras ao invés de mostrar
    # TODO: salvar as fig caso o parametro de save seja true

    def saveMetrics(plot:plt.Figure, path: str, name: str = "imagem", type: str = "png") -> None:
        os.makedirs(path, exist_ok=True)
        plot.savefig(os.path.join(path, f"{name}.{type}"), format=type, bbox_inches='tight')
        plt.close(plot)
        
    def plotAccuracy(self, path: str = "figures") -> Figure:
        fig, ax = plt.subplots()
        ax.plot(self.accuracies, marker='o')
        ax.set_title("Accuracy por Geração")
        ax.set_xlabel("Geração")
        ax.set_ylabel("Accuracy")
        ax.grid(True)

        if self.saveFig:
            self.saveMetrics(fig, path, name="accuracy")

        return fig

    def plotAuroc(self, path: str = "figures"):
        fig, ax = plt.subplots()
        ax.plot(self.aurocs, marker='o', color='orange')
        ax.set_title("AUROC por Geração")
        ax.set_xlabel("Geração")
        ax.set_ylabel("AUROC")
        ax.grid(True)

        if self.saveFig:
            self.saveMetrics(fig, path, name="auroc")
        
        plt.show()

    def plotConfusionMatrixLast(self, path: str = "figures"):
        cm = self.confusion_matrices[-1]
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_title("Matriz de Confusão - Última Geração")
        ax.set_xlabel("Predito")
        ax.set_ylabel("Real")

        if self.saveFig:
            self.saveMetrics(fig, path, name="confusion_matrix")
        
        plt.show()

    def plotPrecision(self):
        plt.plot(self.precisions, marker='o', color='green')
        plt.title("Precision por Geração")
        plt.xlabel("Geração")
        plt.ylabel("Precision")
        plt.grid(True)
        plt.show()

    def plotRecall(self):
        plt.plot(self.recalls, marker='o', color='purple')
        plt.title("Recall por Geração")
        plt.xlabel("Geração")
        plt.ylabel("Recall")
        plt.grid(True)
        plt.show()

    def plotF1Score(self):
        plt.plot(self.f1_scores, marker='o', color='red')
        plt.title("F1 Score por Geração")
        plt.xlabel("Geração")
        plt.ylabel("F1 Score")
        plt.grid(True)
        plt.show()

    def reset(self):
        self.__init__()
