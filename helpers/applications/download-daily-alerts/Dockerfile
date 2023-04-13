FROM ubuntu:latest

RUN set -ex \
	&& apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -yq dos2unix curl awscli \
 	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* 

ENV APPPATH /download-daily-alerts
COPY src $APPPATH
WORKDIR $APPPATH
RUN dos2unix download-daily-alerts.sh
ENTRYPOINT ["bash", "download-daily-alerts.sh"]
