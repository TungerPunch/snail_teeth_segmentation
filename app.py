import os
from flask import Flask, render_template, request, redirect, url_for
from commons import get_image_from_mask
from inference import get_image_and_prediction
import cv2


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return 'There is no file!'
        # Читаем файл
        image_bytes = file.read()
        # Трасформируем к тензору и получаем маску
        image, mask = get_image_and_prediction(image_bytes)
        # Обрезаем изображение по маске
        result = get_image_from_mask(image, mask)
        filepath = os.path.join('static', 'result.png')
        cv2.imwrite(filepath, result)
        return redirect(url_for('show_image', filepath=filepath))
    else:
        return render_template('index.html')

@app.route('/<filepath>',)
def show_image(filepath):
    return render_template("image.html", user_image=filepath)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
    
    
