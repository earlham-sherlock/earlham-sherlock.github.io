FROM ubuntu:16.04

ENV DEBIAN_FRONTEND=noninteractive \
    JAVA_HOME=/usr/lib/jvm/java-8-oracle

COPY jdk-8u191-linux-x64.tar.gz /jdk-8u191-linux-x64.tar.gz

RUN apt-get update && \
    apt-get install -yf wget python apt-utils curl gettext-base && \
    apt-get install -yf telnet inetutils-ping inetutils-telnet inetutils-tools iputils-tracepath && \
    apt-get autoclean -y && \
    apt-get --purge -y autoremove && \
    tar xzf /jdk-8u191-linux-x64.tar.gz -C /tmp && \
    rm -f /jdk-8u191-linux-x64.tar.gz && \
    mkdir -p /usr/lib/jvm && mv /tmp/jdk1.8.0_191 "${JAVA_HOME}" && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    update-alternatives --install "/usr/bin/java" "java" "${JAVA_HOME}/bin/java" 1 && \
    update-alternatives --install "/usr/bin/javac" "javac" "${JAVA_HOME}/bin/javac" 1 && \
    update-alternatives --set java "${JAVA_HOME}/bin/java" && \
    update-alternatives --set javac "${JAVA_HOME}/bin/javac"
