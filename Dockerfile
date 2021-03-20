FROM ubuntu


RUN apt update && \
    apt -y install software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt -y install git python3.7 tk-dev python3-pip libpq-dev python3.7-dev build-essential python3.7-tk

COPY ./backend /app/backend
COPY ./common  /app/common
COPY ./detector /app/detector
COPY ./park_classifier /app/park_classifier
COPY ./slicer /app/app/slicer 
COPY ./spotter /app/spotter
COPY ./requirements.txt /app
COPY ./run_backend.sh /app

ENV PYTHONPATH='/app'

WORKDIR /app
RUN python3.7 -m pip install cython numpy && python3.7 -m pip install -r requirements.txt
#CMD ["yes", ]
CMD ["bash", "run_backend.sh"] 
