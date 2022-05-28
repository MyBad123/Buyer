#syntax=docker/dockerfile:1
FROM ubuntu:18.04

#install russian language
RUN apt-get update && apt-get install -y language-pack-ru
ENV LANGUAGE ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
RUN locale-gen ru_RU.UTF-8 && dpkg-reconfigure locales

#install generic Python prerequisites 
RUN apt-get update && apt-get install -y software-properties-common gcc && \
	add-apt-repository -y ppa:deadsnakes/ppa

#install Python 3.6
RUN apt-get update && apt-get install -y python3.6 python3-distutils python3-pip python3-apt

RUN pip3 install --upgrade pip
RUN pip3 install numpy==1.19.5
RUN pip3 install pandas==0.23.4
RUN pip3 install scipy==1.1.0
RUN pip3 install scikit-learn==0.19.2

COPY classify4.py ./
COPY config.json ./
COPY tbclassifier.py ./
COPY bigdataset.csv ./

EXPOSE 8000
CMD python3 tbclassifier.py
#CMD python3 -m http.server 8000
