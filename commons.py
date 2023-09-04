import io
import albumentations as albu
from albumentations.pytorch import ToTensorV2
import cv2
import numpy as np

import torch


def bytes_to_numpy(image_bytes: bytes) -> np.array:
    '''Трансформирует байтовый файл в np.array'''
    image_bytes = io.BytesIO(image_bytes)
    array = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)
    image = cv2.imdecode(array, 0)
    return image

def transform_image(image: np.array) -> torch.tensor:
    '''Трансформируем изображение в тензор'''
    my_transforms = albu.Compose(
        [
        albu.Resize(512, 512),
        albu.Normalize(mean=(0.449,), std=(0.226,)),
        ToTensorV2()
        ])
    return my_transforms(image=image)['image'].unsqueeze(0)

def detect_largest_poly(mask: np.array) -> np.array:
    '''Находит самый большой контур в маске'''
    # преобразуем изображение в черно-белое
    # находим контуры
    contours, _ = cv2.findContours(mask,
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    # инициализируем переменную для хранения площади наибольшего полигона
    largest_area = 0
    largest_contour = None

    # перебираем все контуры
    for contour in contours:
        # вычисляем площадь текущего полигона
        area = cv2.contourArea(contour)
        # если площадь текущего полигона больше площади наибольшего полигона, то сохраняем его площадь
        if area > largest_area:
            largest_area = area
            largest_contour = contour

    image_copy = np.zeros(mask.shape)
    # копируем текущий полигон в изображение-копию
    cv2.drawContours(image_copy, [largest_contour], -1, 255, cv2.FILLED)
    return image_copy

def get_image_from_mask(image: np.array, mask: np.array) -> np.array:
    '''Обрезает изображение по полученной маске, возвращает '''
    image = image.astype(np.float32)
    image[~mask.astype(bool)] = 0
    # Делаем фон прозрачным
    _,alpha = cv2.threshold(image,0,255,cv2.THRESH_BINARY)
    result = cv2.merge((image, image, image, alpha), 4)
    return result

def postproccesing(mask: np.array) -> np.array:
    '''Находит контур и возвращает к исходному разрешению'''
    mask = detect_largest_poly(mask.astype(np.uint8))
    mask = albu.Resize(1887, 2048)(image=mask)['image']
    return mask