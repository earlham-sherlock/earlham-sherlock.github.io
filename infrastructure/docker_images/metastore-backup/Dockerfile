FROM sherlockdatalake/base:8u212

RUN apt-get install -yf postgresql-client-9.6 s3cmd

COPY ./s3cfg_template /
COPY ./backup.sh /
COPY ./restore.sh /
COPY ./entrypoint.sh /

RUN chmod 777 /*.sh

WORKDIR /

ENTRYPOINT ["/entrypoint.sh"]