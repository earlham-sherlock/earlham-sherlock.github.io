FROM java:openjdk-9-jre

ENV PRESTO_VERSION 0.212

RUN apt-get update && \
    apt-get install -yf python && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    mkdir /opt/presto && \
    curl https://repo1.maven.org/maven2/com/facebook/presto/presto-server/${PRESTO_VERSION}/presto-server-${PRESTO_VERSION}.tar.gz -o presto-server.tar.gz && \
    tar xfz presto-server.tar.gz -C /opt/presto --strip-components=1 && \
    rm presto-server.tar.gz && \
    curl https://repo1.maven.org/maven2/com/facebook/presto/presto-cli/${PRESTO_VERSION}/presto-cli-${PRESTO_VERSION}-executable.jar -o /usr/local/bin/presto-cli && \
    chmod a+x /usr/local/bin/presto-cli

ADD etc /opt/presto/

EXPOSE 8080

ENTRYPOINT ["/opt/presto/bin/launcher", "run"]