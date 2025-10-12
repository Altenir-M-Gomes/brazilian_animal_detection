import os
import logging
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.utils import save_image
from .ImageDataset import ImageDataset

logger = logging.getLogger(__name__)

class TrainDataset:
    def __init__(self, dataPath: str, imageSize: int | tuple[int, int], batchSize: int = 16, verbose: bool = False, verifyImages: bool = False):
        self.dataPath = dataPath
        self.imageSize = imageSize
        self.batchSize = batchSize
        self.trainDatasetPath = os.path.join(dataPath, "train")
        self.testDatasetPath = os.path.join(dataPath, "test")
        self.verbose = verbose 
        self.verifyImages = verifyImages

        if verbose:
            logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    def _buildTrainTransforms(self):
        """
            Cria e retorna o pipeline de transformações aplicado às imagens de treino.

            Esse conjunto de transformações é utilizado para realizar *data augmentation*,
            ou seja, aumentar artificialmente a variedade dos dados de entrada,
            ajudando o modelo a generalizar melhor e evitar overfitting.

            Transformações aplicadas:
                1. Resize(self.imageSize)
                    - Redimensiona a imagem para o tamanho definido (altura, largura).
                2. ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5)
                    - Altera aleatoriamente brilho, contraste e saturação da imagem.
                    - Simula diferentes condições de iluminação e cores.
                3. RandomHorizontalFlip(p=0.5)
                    - Inverte horizontalmente a imagem com 50% de probabilidade.
                    - Ajuda o modelo a reconhecer objetos independentemente da orientação.
                4. RandomVerticalFlip(p=0.1)
                    - Inverte verticalmente a imagem com 10% de probabilidade.
                    - Útil em domínios onde essa variação é válida (ex.: imagens naturais).
                5. RandomRotation(degrees=30)
                    - Rotaciona a imagem aleatoriamente até ±30 graus.
                    - Melhora a robustez do modelo a rotações leves.
                6. ToTensor()
                    - Converte a imagem de PIL ou NumPy array para tensor PyTorch.
                    - Também normaliza os valores de pixel para o intervalo [0, 1].

            Returns:
                torchvision.transforms.Compose:
                    Objeto contendo o pipeline de transformações para o dataset de treino.
        """
        return transforms.Compose([
            transforms.Resize(self.imageSize),
            transforms.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomVerticalFlip(p=0.1),
            transforms.RandomRotation(degrees=30),
            transforms.ToTensor(),
        ])

    def _buildTestTransforms(self):
        """
            Cria e retorna o pipeline de transformações aplicado às imagens de teste.
        
            Diferente do conjunto de treino, aqui **não** são aplicadas transformações aleatórias,
            garantindo que todas as imagens sejam processadas de forma consistente
            e que a avaliação do modelo seja reprodutível.
        
            Transformações aplicadas:
                1. Resize(self.imageSize)
                    - Redimensiona a imagem para o mesmo tamanho utilizado no treino.
                2. ToTensor()
                    - Converte a imagem para tensor PyTorch, normalizando os pixels
                      para o intervalo [0, 1].
        
            Returns:
                torchvision.transforms.Compose:
                    Objeto contendo o pipeline de transformações para o dataset de teste.
        """
        return transforms.Compose([
            transforms.Resize(self.imageSize),
            transforms.ToTensor(),
        ])

    def _createLoader(self, dataset_path: str, transforms, shuffle: bool, num_workers: int, pin_memory: bool):
        """
            Cria e retorna um DataLoader PyTorch para um conjunto de imagens.

            Esta função inicializa um objeto `ImageDataset` com o caminho do diretório
            de imagens e as transformações especificadas, e em seguida cria um `DataLoader`
            configurado com as opções de paralelismo e otimização de memória fornecidas.

            Args:
                dataset_path (str): Caminho para o diretório que contém as imagens
                    do dataset.
                transforms (torchvision.transforms.Compose): Conjunto de transformações
                    aplicadas a cada imagem antes do carregamento (ex: redimensionamento,
                    normalização, data augmentation, etc.).
                shuffle (bool): Define se os dados devem ser embaralhados a cada epoch.
                    Geralmente `True` para treino e `False` para teste.
                num_workers (int): Número de subprocessos usados para carregar os dados.
                    Valores maiores podem acelerar o carregamento em máquinas com múltiplos núcleos.
                pin_memory (bool): Se `True`, move os tensores para uma área de memória
                    fixada (pinned memory), o que pode acelerar a transferência para GPU.

            Returns:
                DataLoader: Objeto PyTorch que fornece os lotes (batches) de imagens
                e rótulos do dataset durante o treinamento ou teste.
        """
        dataset = ImageDataset(dataset_path, transforms=transforms, verbose=self.verbose, verifyImages=self.verifyImages)
        
        if self.verbose:
            logger.info(f"Loaded {len(dataset)} samples from {dataset_path}")
        return DataLoader(dataset, batch_size=self.batchSize, shuffle=shuffle, num_workers=num_workers, pin_memory=pin_memory)

    def loadTrainData(self, num_workers=4, pin_memory=True):    
        '''
            Função que carrega os dados para realizar os treinamentos do modelo de IA, 
            ele já aplica o pipeline de transformações definido para o conjunto de treino chamado _buildTrainTransforms.
            
            Args:
                num_workers (int, optional): Número de subprocessos para carregar os dados. Padrão é 4.
                pin_memory (bool, optional): Se True, os dados carregados serão armazenados em memória fixa. Padrão é True.
            
            Returns:
                DataLoader: Objeto DataLoader do PyTorch contendo os dados de treino prontos para uso.
        '''
        return self._createLoader(self.trainDatasetPath, self._buildTrainTransforms(), True, num_workers, pin_memory)

    def loadTestData(self, num_workers=4, pin_memory=True):
        '''
            Função que carrega os dados para realizar os teste do modelo de IA, 
            ele já aplica o pipeline de transformações definido para o conjunto de teste chamado _buildTestTransforms.
            
            Args:
                num_workers (int, optional): Número de subprocessos para carregar os dados. Padrão é 4.
                pin_memory (bool, optional): Se True, os dados carregados serão armazenados em memória fixa. Padrão é True.
            
            Returns:
                DataLoader: Objeto DataLoader do PyTorch contendo os dados de teste prontos para uso.
        '''
        return self._createLoader(self.testDatasetPath, self._buildTestTransforms(), False, num_workers, pin_memory)

    def saveImageSamples(self, output_dir="samples", num_batches=1):
        """
            Salva amostras de imagens dos conjuntos de treinamento e teste em arquivos de imagem.

            Esta função carrega os DataLoaders de treino e teste, itera sobre um número definido
            de lotes (batches) e salva as imagens em disco no diretório especificado.  
            É útil para inspecionar visualmente se os dados estão sendo carregados e
            transformados corretamente.

            Args:
                output_dir (str, opcional): Caminho do diretório onde as imagens serão salvas.
                    Se o diretório não existir, ele será criado automaticamente.
                    Valor padrão é "samples".
                num_batches (int, opcional): Número de lotes de imagens a serem salvos de cada
                    conjunto (treino e teste). Valor padrão é 1.
            Returns:
                None
        """
        os.makedirs(output_dir, exist_ok=True)
        train_loader = self.loadTrainData()
        test_loader = self.loadTestData()

        for i, (images, _) in enumerate(train_loader):
            save_image(images, f"{output_dir}/train_batch_{i}.jpg")
            if i + 1 >= num_batches: break

        for i, (images, _) in enumerate(test_loader):
            save_image(images, f"{output_dir}/test_batch_{i}.jpg")
            if i + 1 >= num_batches: break

        if self.verbose:
            logger.info(f"Saved {num_batches} batch(es) of train and test images to '{output_dir}'")

    def __str__(self):
        return (
            f"TrainDatasetImplementation("
            f"dataPath='{self.dataPath}', "
            f"imageSize={self.imageSize}, "
            f"batchSize={self.batchSize}, "
            f"trainDatasetPath='{self.trainDatasetPath}', "
            f"testDatasetPath='{self.testDatasetPath}'"
            f")"
        )
