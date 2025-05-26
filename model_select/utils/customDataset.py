import os
import torch
from torch.utils.data import Dataset
from PIL import Image
from PIL import Image

class CustomDataset(Dataset):

    def __init__(self, root_dir, transforms=None):
        # Define the inital variables
        self.root_dir = root_dir
        self.transforms = transforms
        # List sub floder for define class 
        self.classes = os.listdir(root_dir)
        self.classes.sort()
        print("classes name:", self.classes)
        self.images = []
        # For in each sub folder and get the images name folders
        for clc in self.classes:
            images_name = os.listdir(self.root_dir + "/" + clc)
            self.images += [self.root_dir + "/" + clc + "/" + img_name for img_name in images_name]

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        # Take path with index
        image_path = self.images[index]
        # Read image and convert to RGB
        self.verify_image(image_path)
        image = Image.open(image_path).convert("RGB")
        if self.transforms:
            image = self.transforms(image)
        image_class_name = image_path.split("/")[-2]
        label = torch.tensor(self.classes.index(image_class_name))
        return image, label