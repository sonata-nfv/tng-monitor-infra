FROM ubuntu:16.04
LABEL maintainer="Panos Karkazis <pkarkazis@synelixis.com>"

ENV INST_DIR /opt/monitoring/libvirt_exporter/

RUN mkdir -p ${INST_DIR}

RUN apt-get update && apt-get install -y libvirt-dev curl git gcc python3 \
    python3-pip && apt-get clean all

ADD requirements.txt libvirtExporter.py ${INST_DIR}/
WORKDIR ${INST_DIR}
RUN pip3 install -r requirements.txt

CMD [ "python3", "./libvirtExporter.py", "-i ", "2" ]