from typing import List
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from .evalutaionDataClass import EvaluationDataClass
import os

class EvaluationState:
    def __init__(self, saveFig: bool = False):
        self.accuracies: List[float] = []
        self.aurocs: List[float] = []
        self.precisions: List[float] = []
        self.recalls: List[float] = []
        self.f1_scores: List[float] = []
        self.confusion_matrices: List[np.ndarray] = []
        self.classification_reports: List[str] = []
        self.saveFig = saveFig

        # Dados brutos das predições
        self.all_y_true: List[np.ndarray] = []
        self.all_y_pred: List[np.ndarray] = []
        self.all_y_score: List[np.ndarray] = []

        self.saveFig: bool = False

    def appendResult(self, result: EvaluationDataClass):
        self.accuracies.append(result.accuracy)
        self.aurocs.append(result.auroc)
        self.precisions.append(result.precision)
        self.recalls.append(result.recall)
        self.f1_scores.append(result.f1_score)
        self.confusion_matrices.append(result.confusion_matrix)
        self.classification_reports.append(result.classification_report)
        self.all_y_true.append(result.y_true)
        self.all_y_pred.append(result.y_pred)
        self.all_y_score.append(result.y_score)

    def saveMetrics(plot:plt.Figure, path: str, name: str = "imagem", type: str = "png") -> None:
        os.makedirs(path, exist_ok=True)
        plot.savefig(os.path.join(path, f"{name}.{type}"), format=type, bbox_inches='tight')
        plt.close(plot)
        
    def plotAccuracy(self, path: str = "figures"):
        fig, ax = plt.subplots()
        ax.plot(self.accuracies, marker='o')
        ax.set_title("Accuracy por Geração")
        ax.set_xlabel("Geração")
        ax.set_ylabel("Accuracy")
        ax.grid(True)

        if self.saveFig:
            self.saveMetrics(fig, path, name="accuracy")
        
        plt.show()

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
