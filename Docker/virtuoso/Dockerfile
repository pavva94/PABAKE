FROM tenforce/virtuoso:virtuoso7.2.5

RUN apt-get update && apt-get install -y wget

# Add Virtuoso config
COPY virtuoso.ini /virtuoso.ini

# Add startup script
COPY virtuoso.sh /virtuoso.sh


EXPOSE 8890
EXPOSE 1111

VOLUME /data
WORKDIR /data
VOLUME /usr/local/virtuoso-opensource/share/virtuoso/vad/

CMD ["/bin/bash", "/virtuoso.sh"]
