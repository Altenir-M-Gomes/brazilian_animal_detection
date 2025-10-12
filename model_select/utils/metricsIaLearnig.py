import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader
from typing import Tuple
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns
import os
from functools import wraps


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

    def __init__(
        self,
        model: nn.Module,
        device: torch.device,
        testData: DataLoader,
        outPutDim: int = 2,
        savePathFigs: str = "/figures",
        saveFig: bool = False,
        nameModel: str = "unknown",
    ):
        self.nameModel = nameModel
        self.savePathFigs = savePathFigs
        self.saveFig = saveFig
        self.figNumber = 0
        self.model = model
        self.device = device
        self.data = testData
        self.outPutDim = outPutDim
        
        self.yTrue = np.zeros(0, dtype=int)
        self.yPred = np.zeros(0, dtype=int)
        self.yScore = np.empty((0, outPutDim))

        self.accuracy_history = []
        self.precision_history = []
        self.recall_history = []
        self.f1_history = []
        self.auroc_history = []

    def trainTestData(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        self.figNumber += 1
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

        self.yPred = np.concatenate((self.yPred, yPred))
        self.yTrue = np.concatenate((self.yTrue, yTrue))
        self.yScore = np.concatenate((self.yScore, yScore))

        self.accuracy_history.append(self._getAccuracy())
        self.precision_history.append(self._getPrecision())
        self.recall_history.append(self._getRecall())
        self.f1_history.append(self._getF1Score())
        self.auroc_history.append(self._getAuroc())

        return yPred, yTrue, yScore

    @erroWrapper
    def _getAccuracy(self) -> float:
        return accuracy_score(self.yTrue, self.yPred)

    @erroWrapper
    def _getPrecision(self) -> float:
        return precision_score(self.yTrue, self.yPred, average="weighted", zero_division=0)

    @erroWrapper
    def _getRecall(self) -> float:
        return recall_score(self.yTrue, self.yPred, average="weighted", zero_division=0)

    @erroWrapper
    def _getF1Score(self) -> float:
        return f1_score(self.yTrue, self.yPred, average="weighted", zero_division=0)

    @erroWrapper
    def _getConfusionMatrix(self) -> np.ndarray:
        return confusion_matrix(self.yTrue, self.yPred)

    @erroWrapper
    def _getAuroc(self) -> float:
        if len(self.yScore.shape) == 2:
            if self.yScore.shape[1] == 2:
                return roc_auc_score(self.yTrue, self.yScore[:, 1])
            else:
                return roc_auc_score(self.yTrue, self.yScore, multi_class="ovr", average="weighted")
        else:
            return roc_auc_score(self.yTrue, self.yScore)

    @erroWrapper
    def _classificationReport(self) -> str | dict:
        return classification_report(self.yTrue, self.yPred)

    def __str__(self) -> str:
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

    def saveMetrics(self, plot: plt.Figure, path: str = "figures", name: str = "imagem", figNumber: int = 0, type: str = "png") -> None:
        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(os.path.dirname(current_file))
        safe_path = path.lstrip("/")
        save_dir = os.path.join(base_dir, safe_path, getattr(self, "nameModel", "default_model"))
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{name}_epoch{figNumber}.{type}")
        plot.savefig(save_path, format=type, bbox_inches="tight")
        plt.close(plot)

    def _plotGeneric(self, values, title, ylabel, color, name):
        if not values:
            print(f"[WARNING] Nenhum dado para plotar em {name}")
            return None

        fig, ax = plt.subplots()
        ax.plot(range(1, len(values) + 1), values, color=color)
        ax.set_title(title)
        ax.set_xlabel("Geração")
        ax.set_ylabel(ylabel)
        ax.grid(True)

        if self.saveFig:
            self.saveMetrics(fig, path=self.savePathFigs, name=name, figNumber=self.figNumber)

        return fig

    def _plotAccuracy(self): return self._plotGeneric(self.accuracy_history, "Accuracy por Geração", "Accuracy", "blue", "accuracy")
    def _plotAuroc(self): return self._plotGeneric(self.auroc_history, "AUROC por Geração", "AUROC", "orange", "auroc")
    def _plotPrecision(self): return self._plotGeneric(self.precision_history, "Precision por Geração", "Precision", "green", "precision")
    def _plotRecall(self): return self._plotGeneric(self.recall_history, "Recall por Geração", "Recall", "purple", "recall")
    def _plotF1Score(self): return self._plotGeneric(self.f1_history, "F1 Score por Geração", "F1 Score", "red", "f1_score")

    def _plotConfusionMatrix(self):
        cm = self._getConfusionMatrix()
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_title("Matriz de Confusão")
        ax.set_xlabel("Predito")
        ax.set_ylabel("Real")
        if self.saveFig:
            self.saveMetrics(fig, path=self.savePathFigs, name="confusion_matrix", figNumber=self.figNumber)
        plt.show()
        return fig

    def showAll(self):
        for plot_func in [self._plotAccuracy, self._plotAuroc, self._plotConfusionMatrix, self._plotPrecision, self._plotRecall, self._plotF1Score]:
            fig = plot_func()
            if fig:
                plt.show(fig)
