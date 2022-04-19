#!/bin/bash

rm -rf $1/boot
cp -r $PUSHPY_START_HOME/boot $1/boot

rm -rf $1/conf
cp -r $PUSHPY_START_HOME/conf $1/conf

cp $PUSHPY_START_HOME/deploy/monitor.py $1

# build the composite requirements.txt
$1/mkreq.sh $1

source $1/config.sh

maintainer="$DOCKER_IMAGE_MAINTAINER"
imagename="$DOCKER_IMAGE_NAME"

cd ..
tag=$(cat setup.py | grep "version=" | sed -e 's/"/ /g' | awk '{print $2}')

echo ""
echo "--------------------------------------------------------"
echo "Building new Docker image(${maintainer}/${imagename})"
cd docker
docker build --no-cache --rm -t $maintainer/$imagename $*
last_status=$?
if [[ "${last_status}" == "0" ]]; then
    echo ""
    if [[ "${tag}" != "" ]]; then
        image_csum=$(docker images | grep "${maintainer}/${imagename} " | grep latest | awk '{print $3}')
        if [[ "${image_csum}" != "" ]]; then
            docker tag $image_csum $maintainer/$imagename:$tag
            docker tag $maintainer/$imagename:$tag eismcc/$imagename:$tag
            last_status=$?
            if [[ "${last_status}" != "0" ]]; then
                echo "Failed to tag image(${imagename}) with Tag(${tag})"
                echo ""
                exit 1
            else
                echo "Build Successful Tagged Image(${imagename}) with Tag(${tag})"
            fi

            echo ""
            exit 0
        else
            echo ""
            echo "Build failed to find latest image(${imagename}) with Tag(${tag})"
            echo ""
            exit 1
        fi
    else
        echo "Build Successful"
        echo ""
        exit 0
    fi
    echo ""
else
    echo ""
    echo "Build failed with exit code: ${last_status}"
    echo ""
    exit 1
fi

exit 0
