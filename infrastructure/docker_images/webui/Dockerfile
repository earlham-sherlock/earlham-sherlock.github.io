FROM sherlockdatalake/base:8u212

ARG YANAGISHIMA_VERSION=21.0

RUN mkdir /build && \
    cd /build && \
    curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh && \
    bash nodesource_setup.sh && \
    apt update && \
    apt install -y nodejs && \
    git clone https://github.com/yanagishima/yanagishima && \
    cd /build/yanagishima && \
    git checkout refs/tags/$YANAGISHIMA_VERSION && \
    cd /build/yanagishima/web && \
    npm install && \
    npm run build && \
    cd /build/yanagishima && \
    ./gradlew :distZip && \
    mkdir /app && \
    cd /app && \
    mv /build/yanagishima/build/distributions/yanagishima-$YANAGISHIMA_VERSION.zip /app/yanagishima-$YANAGISHIMA_VERSION.zip && \
    unzip yanagishima-$YANAGISHIMA_VERSION.zip && \
    mv yanagishima-$YANAGISHIMA_VERSION yanagishima && \
    mkdir -p /app/yanagishima/conf && \
    mkdir -p /app/yanagishima/data && \
    rm -f yanagishima-$YANAGISHIMA_VERSION.zip && \
    rm -rf /build && \
    apt purge nodejs -y && \
    apt-get autoclean -y && \
    apt-get --purge -y autoremove

ADD yanagishima.properties /app/yanagishima/conf/yanagishima.properties

ADD entrypoint.sh /app/yanagishima/entrypoint.sh

EXPOSE 8080

WORKDIR /app/yanagishima

ENTRYPOINT ["bash", "/app/yanagishima/entrypoint.sh"]

# TUDO: backup /app/yanagishima/data folder
