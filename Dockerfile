FROM python:3.10.4-slim
ENV FLASK_APP=main
ENV FLASK_ENVIRONMENT=production

WORKDIR /app

RUN apt-get install wget
RUN wget -O yolov4-csp.weights "https://docs.google.com/uc?export=download&confirm=t&id=1V3vsIaxAlGWvK4Aar9bAiK5U0QFttKwq"

RUN git clone "https://github.com/AlexeyAB/darknet" darknet
WORKDIR /app/darknet
RUN make

WORKDIR /app

COPY ./obj-detect-venv/ .
COPY requirements.txt .

RUN source ./obj-detect-venv/bin/activate
RUN pip install -r requirements.txt

CMD ["flask", "run"]