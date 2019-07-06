FROM openjdk:11.0.3-jdk-stretch

ARG YANAGISHIMA_VERSION=21.0

RUN mkdir /build && \
    cd /build && \
    curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh && \
    bash nodesource_setup.sh && \
    apt install -y nodejs && \
    git clone https://github.com/yanagishima/yanagishima && \
    cd /build/yanagishima && \
    git checkout refs/tags/$YANAGISHIMA_VERSION && \
    ./gradlew :distZip && \
    mkdir /app && \
    cd /app && \
    mv /build/yanagishima/build/distributions/yanagishima-$YANAGISHIMA_VERSION.zip /app/yanagishima-$YANAGISHIMA_VERSION.zip && \
    unzip yanagishima-$YANAGISHIMA_VERSION.zip && \
    mv yanagishima-$YANAGISHIMA_VERSION yanagishima && \
    rm -f yanagishima-$YANAGISHIMA_VERSION.zip && \
    rm -rf /build && \
    apt purge nodejs -y && \
    apt-get autoclean -y && \
    apt-get --purge -y autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get -y install gettext-base && \
    apt-get autoclean -y && \
    apt-get --purge -y autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD yanagishima.properties /app/yanagishima/conf/yanagishima.properties

ADD entrypoint.sh /app/yanagishima/entrypoint.sh

EXPOSE 8080

WORKDIR /app/yanagishima

ENTRYPOINT ["bash", "/app/yanagishima/entrypoint.sh"]

# TUDO: backup /app/yanagishima/data folder
