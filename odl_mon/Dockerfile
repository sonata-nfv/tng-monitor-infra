FROM ubuntu:14.04

RUN apt-get update && apt-get -y upgrade && \
apt-get -y install apache2 python2.7 libmysqlclient-dev python2.7-dev python-pip nano && \ 
mkdir -p /opt/Monitoring

COPY ./vm_mon/ /opt/Monitoring

ADD ./vm_mon/run.sh /opt/Monitoring/run.sh
RUN chmod 0755 /opt/Monitoring/run.sh
RUN ls -la /opt/Monitoring/*

CMD ["/opt/Monitoring/run.sh"]

