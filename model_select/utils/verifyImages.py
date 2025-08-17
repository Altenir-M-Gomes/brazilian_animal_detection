import os
from PIL import Image

class VerifyImages:

    def __init__(self, path: str):
        self.path = path
        self.train = f"{path}/train"
        self.test = f"{path}/test"

    def checkImages(self, path, fname):
        try:
            img = Image.open(path)
            img.load()  # força o carregamento
            img.close()
            return None  # imagem válida
        except Exception as e:
            print(f"Corrompida: {fname} -> {e}")
            return path  # ou fname, se quiser só o nome

    
    def verifyFloaders(self, floader:str) -> list[str]:
        corrupted = []
        for subFloader in ['com_animal', 'sem_animal']:
            for root, _, files in os.walk(f'{floader}/{subFloader}'):
                for fname in files:
                    if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                        path = os.path.join(root, fname)
                        result = self.checkImages(path, fname)
                        if result != None:
                            corrupted.append(result)
        return corrupted
    
    def verifyTrainAndTest(self):
        trainCorrupted = self.verifyFloaders(f'{self.path}/train')
        testCorrupted = self.verifyFloaders(f'{self.path}/test')
        print(f"Imagens corrompidas do dataset train: {trainCorrupted}")
        print(f"Imagens corrompidas do dataset test: {testCorrupted}")

