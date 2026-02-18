FROM eclipse-temurin:11-jdk-jammy AS build

ARG YANAGISHIMA_VERSION=21.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git gnupg unzip \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" > /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /build \
    && cd /build \
    && git clone https://github.com/yanagishima/yanagishima \
    && cd /build/yanagishima \
    && git checkout "refs/tags/${YANAGISHIMA_VERSION}" \
    && ./gradlew :distZip \
    && mkdir -p /out \
    && cp "/build/yanagishima/build/distributions/yanagishima-${YANAGISHIMA_VERSION}.zip" /out/yanagishima.zip


FROM eclipse-temurin:11-jre-jammy

RUN apt-get update \
    && apt-get install -y --no-install-recommends gettext-base unzip \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /out/yanagishima.zip /tmp/yanagishima.zip
RUN mkdir -p /app \
    && cd /app \
    && unzip /tmp/yanagishima.zip \
    && rm -f /tmp/yanagishima.zip \
    && mv /app/yanagishima-* /app/yanagishima

ADD yanagishima.properties /app/yanagishima/conf/yanagishima.properties

ADD entrypoint.sh /app/yanagishima/entrypoint.sh

EXPOSE 8080

WORKDIR /app/yanagishima

ENTRYPOINT ["bash", "/app/yanagishima/entrypoint.sh"]

# TODO: backup /app/yanagishima/data folder
