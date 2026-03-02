# Use Debian stable slim
FROM debian:stable-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    build-essential \
    wget \
    xz-utils \
    redis-tools \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.13 (official source build)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    libncursesw5-dev \
    libgdbm-dev \
    liblzma-dev \
    tk-dev \
    uuid-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

RUN wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz \
    && tar -xzf Python-3.13.0.tgz \
    && cd Python-3.13.0 \
    && ./configure --enable-optimizations --with-ensurepip=install \
    && make -j"$(nproc)" \
    && make altinstall \
    && cd / \
    && rm -rf /tmp/Python-3.13.0*

# Create symlinks
RUN ln -s /usr/local/bin/python3.13 /usr/local/bin/python \
    && ln -s /usr/local/bin/pip3.13 /usr/local/bin/pip

# Install Node.js 24.14.0
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && rm -rf /var/lib/apt/lists/*

# Verify versions 
RUN python --version \
    && pip --version \
    && node --version \
    && npm --version \
    && redis-cli --version \
    && mysql --version

# Default working directory
WORKDIR /workspace

CMD [ "bash" ]