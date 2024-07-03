FROM python:3.12.2

WORKDIR /app

ADD inferencing.py .
ADD XDreamv1(m).pt .

RUN pip install ultralytics==8.1.34
RUN pip install opencv_python==4.10.0.82

CMD ["python", "inferencing.py"]