.PHONY: build build-light build-full
.PHONY: push push-light push-full
.PHONY: run run-light run-full run-base

IM_NAME=dimitrivinet/latex_offline
VERSION=v1.1.0
IM_TAG_LIGHT=${VERSION}-light
IM_TAG_EXTRA=${VERSION}-extra
IM_TAG_FULL=${VERSION}-full
CONTAINER_NAME=latex_offline

IM_BASE=debian:buster

TEST_ASSET=$(shell pwd)/../test_assets/work

build: build-light build-full

build-light:
	docker build -t ${IM_NAME}:${IM_TAG_LIGHT} --build-arg BASE=light .

build-extra:
	docker build -t ${IM_NAME}:${IM_TAG_EXTRA} --build-arg BASE=extra .

build-full:
	docker build -t ${IM_NAME}:${IM_TAG_FULL} --build-arg BASE=full .

push: push-light push-full

push-light:
	docker push ${IM_NAME}:${IM_TAG_LIGHT}

push-extra:
	docker push ${IM_NAME}:${IM_TAG_EXTRA}

push-full:
	docker push ${IM_NAME}:${IM_TAG_FULL}

run: run-full

run-light:
	docker run -it --rm \
	--name ${CONTAINER_NAME} \
	-e LOCAL_USER_ID=$(shell id -u ${USER}) \
	-v ${TEST_ASSET}:/data \
	${IM_NAME}:${IM_TAG_FULL} \
	bash

run-full:
	docker run -it --rm \
	--name ${CONTAINER_NAME} \
	-e LOCAL_USER_ID=$(shell id -u ${USER}) \
	-v ${TEST_ASSET}:/data \
	${IM_NAME}:${IM_TAG_FULL} \
	bash

run-base:
	docker run -it --rm \
	--name ${CONTAINER_NAME} \
	-v ${TEST_ASSET}:/data \
	${IM_BASE} \
	bash
