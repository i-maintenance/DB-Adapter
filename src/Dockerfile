FROM python:3.5.4

# test internet connection and dns settings. If apt-get update fails, restart 
# docker service, check internet connection and dns settings in /etc/docker/daemon.json
#RUN apt-get update

# install librdkafka client
ARG LIBRDKAFKA_VERSION
RUN apt-get update && \
    git clone https://github.com/edenhill/librdkafka && cd librdkafka && \
    git checkout v${LIBRDKAFKA_VERSION} && \
    ./configure && make && make install && ldconfig

# install confluent-kafka-client
ARG CONFLUENT_KAFKA_VERSION
RUN pip install confluent-kafka==${CONFLUENT_KAFKA_VERSION}

RUN mkdir /home/src
WORKDIR /home/src
ADD requirements.txt /home/src
RUN pip install -r /home/src/requirements.txt

ADD db-adapter.py /home/src

CMD ["python", "/home/src/db-adapter.py"]
