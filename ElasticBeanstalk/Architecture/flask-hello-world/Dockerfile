FROM ubuntu:latest

RUN set -ex \
	&& apt-get update \
	&& apt-get install -y \
 			python3-pip \
 			python3-dev \
 			build-essential \
 	&& apt-get clean \
 	&& rm -rf /var/lib/apt/lists/* 

ENV APPPATH /flask-hello-world
COPY src/requirements.txt $APPPATH/requirements.txt
WORKDIR $APPPATH
RUN pip3 --disable-pip-version-check install -r requirements.txt
COPY src/web $APPPATH/web
ENTRYPOINT ["python3"]
CMD ["web/app.py"]