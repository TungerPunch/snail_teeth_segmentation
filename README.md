# Веб-приложения c применением глубокого обучения для сегментации и обрезки зуб улиток с микроскопа(for my dear Daria)
Модель - Unet. Препроцессинг, постпроцессинг был выполнен с помощью opencv. Альбументация применена с помощью библиотеки Albumentation.
Код обучения модели и постпроцессинга находится в model_and_postprocessing.ipynb и:
https://colab.research.google.com/drive/17Ir7MkmpraJgx6nsvi5EOB2vXR5CxoeR#scrollTo=kLxWtFTTQBnI


Маски создавались с помощью уже обрезанных фотографий в teeth_mask_creation.ipynb


Результат обработки можно увидеть в static

Для запуска приложения введите в командной строке python app.py
