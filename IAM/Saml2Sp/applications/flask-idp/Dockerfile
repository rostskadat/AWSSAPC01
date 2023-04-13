FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
RUN set -ex \
	&& apt-get update \
	&& apt-get install --no-install-recommends --yes \
 			python3-pip \
 			python3-dev \
 			build-essential \
			xmlsec1 \
			libxmlsec1-openssl \
			curl \
 	&& apt-get clean \
 	&& rm -rf /var/lib/apt/lists/* 

ENV APPPATH /flask-idp
COPY requirements.txt $APPPATH/requirements.txt
WORKDIR $APPPATH
RUN pip3 --disable-pip-version-check install -r requirements.txt
COPY idp2 $APPPATH
EXPOSE 8088/tcp
CMD ["python3", "-u", "idp.py", "idp_conf"]