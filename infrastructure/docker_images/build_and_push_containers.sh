#!/usr/bin/env bash

set -e

build_image () {
    cd $1 > /dev/null
    name=`basename $1`

    echo -e "\n======="
    echo -e "======= building image: $name"
    echo -e "=======\n"

    if [ ! -f Dockerfile ]; then
        echo -e "\n======= ERROR: No Dockerfile found! (${1}Dockerfile)\n"
        cd - > /dev/null
        return 1
    fi


    if [ ! -f image_version ]; then
        echo -e "======= WARNING: No image_version file found, falling back to default tag: latest\n"
        version="latest"
    else
        version=$(head -n 1 image_version)
        echo -e "======= image_version file found, using tag: ${version}\n"
    fi

    docker build --tag ${name}:${version} ./

    echo -e "\n======="
    echo -e "======= pushing image: $name:${version}"
    echo -e "=======\n"


    docker tag ${name}:${version} bbazsi41/$name:${version}
    docker push bbazsi41/$name:${version}

    cd - > /dev/null
}


# first make sure the base image is built
build_image "./base"

# then build all other images
for d in ./*/ ; do
    if [ `basename $d` != "base" ]; then
        build_image $d
    fi
done


echo -e "\n======= finished :) \n"