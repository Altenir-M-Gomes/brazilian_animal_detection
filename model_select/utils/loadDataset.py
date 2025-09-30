
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.utils import save_image
from .ImageDataset import ImageDataset

class TrainDatasetImplemetation:
    
    def __init__(self, data_path, image_size, batch_size=16):
        # Convert image to PIL
        self.to_pill = transforms.ToPILImage()
        # Resize image to the size parameter
        self.resize_img = transforms.Resize(image_size)
        # Create color variation for import ia 
        self.color_jitter = transforms.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5)
        # Horizontally flips the image with a 50% probability 
        self.flip_horizontal = transforms.RandomHorizontalFlip(p=0.5)
        # Vertically flips the image with a 10% probability.
        self.flip_vertical = transforms.RandomVerticalFlip(p=0.1)
        # Rotates the image randomly within ±30 degrees.
        self.random_rotation = transforms.RandomRotation(degrees=30)
        # Converts the image to a tensor for PyTorch models.
        self.to_tensor = transforms.ToTensor()
        # Create the train and test dataset path
        self.train_dataset_path = data_path + "/train"
        self.test_dataset_path = data_path + "/test"
        # Create the batch size
        self.batch_size = batch_size

    def report_size_img(self, train_data, test_data):
        for data in train_data:
            images, labels = data
            print("train images shape:", images.shape)
            print("train labels:", labels)
            break

        for data in test_data:
            images, labels = data
            print("test images shape:", images)
            print("test labels:", labels)
            print("test images shape:", images.shape)
            print("test labels:", labels)
            break

    def load_train_data(self, num_workers=4, pin_memory=True):
        transforms_train = transforms.Compose([ 
            self.resize_img, 
            self.color_jitter, 
            self.flip_horizontal, 
            self.flip_vertical, 
            self.random_rotation, 
            self.to_tensor
        ])
        
        train_dataset = ImageDataset(self.train_dataset_path, transforms=transforms_train)
        print("no of samples in train dataset", len(train_dataset))

        train_loader = DataLoader(
            train_dataset, 
            batch_size=self.batch_size, 
            shuffle=True, 
            num_workers=num_workers, 
            pin_memory=pin_memory
        )

        self.report_size_img(train_loader, [])
        return train_loader


    def load_test_data(self, num_workers=4, pin_memory=True):
        transforms_test = transforms.Compose([
            self.resize_img,
            self.to_tensor
        ])
        
        test_dataset = ImageDataset(self.test_dataset_path, transforms=transforms_test)
        print("no of samples in test dataset", len(test_dataset))

        test_loader = DataLoader(
            test_dataset, 
            batch_size=self.batch_size, 
            shuffle=True, 
            num_workers=num_workers, 
            pin_memory=pin_memory
        )

        self.report_size_img([], test_loader)
        return test_loader

    def save_image(self):
        train_data, test_data = self.load_data()
        self.report_size_img(train_data, test_data)

        for data in train_data:
            images, labels = data
            save_image(images, "images_train.jpg")
            break

        for data in test_data:
            images, labels = data
            print("test images shape:", images.shape)
            print("test labels:", labels)
            save_image(images, "images_test.jpg")
            break
