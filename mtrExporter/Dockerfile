FROM python:3.6-jessie

ADD sources.list /etc/apt/sources.list
RUN apt-get update && apt-get -y upgrade && \
apt-get -y install cron apache2 python3 libmysqlclient-dev python3-dev python3-setuptools nano && \ 
mkdir -p /opt/Monitoring

COPY ./ /opt/Monitoring
RUN pip3 install -r /opt/Monitoring/requirements.txt

ADD ./run.sh /opt/Monitoring/run.sh
RUN chmod 0755 /opt/Monitoring/run.sh
RUN chmod 0755 /opt/Monitoring/checkservice.sh
RUN ls -la /opt/Monitoring/*

CMD ["/opt/Monitoring/run.sh"]