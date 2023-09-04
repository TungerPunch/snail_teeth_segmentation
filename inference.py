from commons import bytes_to_numpy, transform_image, postproccesing
import cv2
import torch

# Загружаем модель
path_to_weights = r'.\best_model.pth'
model = torch.load(path_to_weights,
                   map_location='cpu')


def get_image_and_prediction(image_bytes):
    image = bytes_to_numpy(image_bytes)
    eq_image = cv2.equalizeHist(image)
    tensor = transform_image(eq_image)
    mask = model(tensor).detach().squeeze().numpy().round()
    mask = postproccesing(mask)
    return image, mask
