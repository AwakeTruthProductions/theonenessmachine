FROM python:3.7.4-alpine

RUN apk --no-cache add python python3 \
    build-base \
    python-dev python3-dev \
    # wget dependency
    openssl \
    # dev dependencies
    git \
    bash \
    sudo \
    py2-pip \
    # Pillow dependencies
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    harfbuzz-dev \
    fribidi-dev && \
    rm -rf /var/cache/apk/*
RUN mkdir -p /scripts/var/awaken
COPY . /scripts/var/awaken
WORKDIR /scripts/var/awaken
RUN pip install --user --upgrade setuptools
RUN pip install -r requirements.txt
RUN export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
CMD python3 -m theonenessmachine