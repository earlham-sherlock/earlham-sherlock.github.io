FROM openjdk:8u212-jdk

ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i \
            -e 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' \
            -e 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' \
            /etc/apt/sources.list \
        && sed -i '/stretch-updates/d' /etc/apt/sources.list \
        && rm -f /etc/apt/sources.list.d/* \
        && printf 'Acquire::Check-Valid-Until "false";\n' > /etc/apt/apt.conf.d/99no-check-valid-until \
        && printf 'Acquire::AllowInsecureRepositories "true";\nAcquire::AllowDowngradeToInsecureRepositories "true";\nAPT::Get::AllowUnauthenticated "true";\n' > /etc/apt/apt.conf.d/99allow-insecure-archive \
        && apt-get -o Acquire::Check-Valid-Until=false -o Acquire::AllowInsecureRepositories=true -o Acquire::AllowDowngradeToInsecureRepositories=true update && \
        apt-get install -y --allow-unauthenticated wget python apt-utils curl gettext-base less vim mc && \
        apt-get install -y --allow-unauthenticated telnet inetutils-ping inetutils-telnet inetutils-tools iputils-tracepath && \
    apt-get autoclean -y && \
    apt-get --purge -y autoremove
