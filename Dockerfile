FROM python:3.8-slim-buster

RUN pip install --upgrade pip
RUN pip install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python app.py