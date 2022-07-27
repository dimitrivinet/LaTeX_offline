.PHONY: build run

IM_NAME=latex_offline
IM_TAG=dev
CONTAINER_NAME=latex_offline

IM_BASE=debian:buster

TEST_ASSET=$(shell pwd)/test_assets/work

build:
	docker build -t ${IM_NAME}:${IM_TAG} .

run:
	docker run -it --rm \
	--name ${CONTAINER_NAME} \
	-e LOCAL_USER_ID=$(shell id -u ${USER}) \
	-v ${TEST_ASSET}:/data \
	${IM_NAME}:${IM_TAG} \
	bash

run-base:
	docker run -it --rm \
	--name ${CONTAINER_NAME} \
	-v ${TEST_ASSET}:/data \
	${IM_BASE} \
	bash
