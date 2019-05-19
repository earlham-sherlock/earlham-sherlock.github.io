FROM openjdk:8u212-jdk

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -yf wget python apt-utils curl gettext-base less vim mc && \
    apt-get install -yf telnet inetutils-ping inetutils-telnet inetutils-tools iputils-tracepath && \
    apt-get autoclean -y && \
    apt-get --purge -y autoremove
