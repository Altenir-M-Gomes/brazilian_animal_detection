from dataclasses import dataclass
import numpy as np
from typing import Union

@dataclass
class EvaluationDataClass:
    accuracy: float
    auroc: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: np.ndarray
    classification_report: str
    y_true: Union[np.ndarray, list]
    y_pred: Union[np.ndarray, list]
    y_score: Union[np.ndarray, list]
