ARG BASE=light
# use base step since texlive takes a long time to install
# it is not recommended to change this step
FROM debian:buster as base

# installing utils
RUN : \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
        git make curl wget nano \
        python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && :

FROM base as light

RUN : \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
        texlive \
    && rm -rf /var/lib/apt/lists/* \
    && :

FROM base as extra

RUN : \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
        texlive texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/* \
    && :

FROM base as full

RUN : \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
        texlive-full \
    && rm -rf /var/lib/apt/lists/* \
    && :

FROM ${BASE}

RUN : \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
        gosu \
        # other latex
        latexmk \
        # for nodemon
        software-properties-common npm \
    && rm -rf /var/lib/apt/lists/* \
    && :

ARG NODE_VERSION=16.16.0

RUN : \
    && npm install npm@$lts -g \
    && npm install n -g \
    && n ${NODE_VERSION} \
    && /usr/local/n/versions/node/${NODE_VERSION}/bin/npm install -g nodemon \
    && :

RUN mkdir /data
RUN mkdir /nodemon_config

COPY nodemon_config /nodemon_config

VOLUME /data

WORKDIR /data

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]
