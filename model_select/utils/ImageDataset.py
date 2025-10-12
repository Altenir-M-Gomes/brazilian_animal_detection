import os
import torch
import logging
from typing import List, Optional
from torch.utils.data import Dataset
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)

class ImageDataset(Dataset):
    """
    Dataset personalizado para carregar imagens organizadas em subpastas,
    onde cada subpasta representa uma classe.

    Além de carregar as imagens, esta classe também pode verificar e ignorar
    automaticamente arquivos corrompidos.
    """

    def __init__(self, root_dir: str, transforms=None, verifyImages: bool = False, verbose: bool = False):
        """
        Inicializa o dataset, opcionalmente verificando imagens corrompidas.

        Estrutura esperada do diretório:
            root_dir/
            ├── classe_1/
            │   ├── img1.jpg
            │   ├── img2.jpg
            ├── classe_2/
            │   ├── img3.jpg
            │   ├── img4.jpg

        Args:
            root_dir (str): Caminho do diretório raiz contendo as classes e imagens.
            transforms (callable, opcional): Transformações a serem aplicadas em cada imagem.
            verifyImages (bool, opcional): Se True, verifica e ignora imagens corrompidas. Padrão: True.
            verbose (bool, opcional): Se True, exibe logs detalhados durante o carregamento.
        """
        self.root_dir = root_dir
        self.transforms = transforms
        self.verifyImages = verifyImages
        self.verbose = verbose

        if verbose:
            logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

        # Lista as classes (subpastas)
        self.classes = sorted([
            d for d in os.listdir(root_dir)
            if os.path.isdir(os.path.join(root_dir, d))
        ])

        self.images = self._loadImages()

    def _isImageCorrupted(self, file_path: str) -> bool:
        """
        Verifica se uma imagem está corrompida tentando abri-la com Pillow.

        Args:
            file_path (str): Caminho completo da imagem.

        Returns:
            bool: True se estiver corrompida, False se estiver válida.
        """
        try:
            with Image.open(file_path) as img:
                img.verify()
            return False
        except (UnidentifiedImageError, OSError, ValueError) as e:
            if self.verbose:
                logger.warning(f"Imagem corrompida ignorada: {file_path} ({e})")
            return True

    def _loadImages(self) -> List[str]:
        """
        Percorre as subpastas do dataset e coleta os caminhos de todas as imagens válidas.

        Returns:
            List[str]: Lista com os caminhos completos das imagens.
        """
        image_paths: List[str] = []
        valid_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")

        for class_name in self.classes:
            class_dir = os.path.join(self.root_dir, class_name)
            for fname in os.listdir(class_dir):
                if fname.lower().endswith(valid_extensions):
                    file_path = os.path.join(class_dir, fname)

                    if self.verifyImages and self._isImageCorrupted(file_path):
                        continue 

                    image_paths.append(file_path)

        if self.verbose:
            logger.info(f"Dataset '{self.root_dir}' carregado com {len(image_paths)} imagens válidas.")
        return image_paths

    def __len__(self) -> int:
        """Retorna o número total de imagens válidas no dataset."""
        return len(self.images)

    def __getitem__(self, index: int):
        """
        Retorna uma tupla (imagem, label) para o índice especificado.

        Args:
            index (int): Índice da amostra desejada.

        Returns:
            tuple(torch.Tensor, torch.Tensor):
                - Imagem transformada
                - Label (tensor com o índice da classe)
        """
        image_path = self.images[index]
        class_name = image_path.split(os.sep)[-2]
        label = torch.tensor(self.classes.index(class_name))

        image = Image.open(image_path).convert("RGB")
        if self.transforms:
            image = self.transforms(image)

        return image, label

    def verifyTrainAndTest(self) -> None:
        """
        Verifica manualmente imagens corrompidas em 'train' e 'test'
        dentro do mesmo diretório raiz.
        """
        for subset in ["train", "test"]:
            subset_path = os.path.join(self.root_dir, subset)
            if not os.path.exists(subset_path):
                logger.warning(f"Subpasta '{subset}' não encontrada em {self.root_dir}")
                continue

            corrupted_files = self._verifyDirectory(subset_path)
            msg = f"Total de imagens corrompidas em '{subset}': {len(corrupted_files)}"
            logger.info(msg)

            if corrupted_files:
                logger.info("Lista de imagens corrompidas:")
                for f in corrupted_files:
                    logger.info(f"  - {f}")

    def _verifyDirectory(self, directory: str) -> List[str]:
        """Método auxiliar que varre um diretório específico e retorna imagens corrompidas."""
        corrupted: List[str] = []
        for root, _, files in os.walk(directory):
            for fname in files:
                if fname.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")):
                    file_path = os.path.join(root, fname)
                    if self._is_image_corrupted(file_path):
                        corrupted.append(file_path)
        return corrupted

    def __str__(self) -> str:
        """Retorna uma representação legível da instância."""
        return (
            f"ImageDataset("
            f"root_dir='{self.root_dir}', "
            f"num_classes={len(self.classes)}, "
            f"num_images={len(self.images)}, "
            f"verifyImages={self.verifyImages}"
            f")"
        )
