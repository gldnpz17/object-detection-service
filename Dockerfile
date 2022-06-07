FROM python:3.10.4
ENV FLASK_APP=main
ENV FLASK_ENVIRONMENT=production

WORKDIR /app

#RUN apt-get update
#RUN apt-get install wget -y
RUN wget -O yolov4-csp.weights "https://docs.google.com/uc?export=download&confirm=t&id=1V3vsIaxAlGWvK4Aar9bAiK5U0QFttKwq"

#RUN apt-get install git -y
RUN git clone "https://github.com/AlexeyAB/darknet" darknet
WORKDIR /app/darknet
#RUN apt-get install make -y
RUN make

WORKDIR /app

COPY ./obj-detect-venv/ .
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run"]