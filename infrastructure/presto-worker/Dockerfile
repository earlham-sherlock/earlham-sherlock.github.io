FROM sherlockdatalake/base:8u191

ENV PRESTO_VERSION 0.213

RUN mkdir /opt/presto && \
    curl https://repo1.maven.org/maven2/com/facebook/presto/presto-server/${PRESTO_VERSION}/presto-server-${PRESTO_VERSION}.tar.gz -o presto-server.tar.gz && \
    tar xfz presto-server.tar.gz -C /opt/presto --strip-components=1 && \
    rm presto-server.tar.gz && \
    curl https://repo1.maven.org/maven2/com/facebook/presto/presto-cli/${PRESTO_VERSION}/presto-cli-${PRESTO_VERSION}-executable.jar -o /usr/local/bin/presto-cli && \
    chmod a+x /usr/local/bin/presto-cli

ADD etc /opt/presto/etc
ADD entrypoint.sh /entrypoint.sh

#ENTRYPOINT ["/opt/presto/bin/launcher", "run"]
ENTRYPOINT ["bash", "/entrypoint.sh"]
#CMD ["/opt/presto/bin/launcher", "run"]