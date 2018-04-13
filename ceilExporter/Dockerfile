FROM ubuntu:16.04

RUN apt-get update && apt-get -y upgrade && \
apt-get -y install apache2 python3 libmysqlclient-dev python3-dev python-pip3 nano && \ 
mkdir -p /opt/Monitoring

COPY ./ceilExporter/ /opt/Monitoring

ADD ./ceilExporter/run.sh /opt/Monitoring/run.sh
RUN chmod 0755 /opt/Monitoring/run.sh
RUN ls -la /opt/Monitoring/*

CMD ["/opt/Monitoring/run.sh"]