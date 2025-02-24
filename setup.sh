#!/usr/bin/env bash

set -e

if [ ! -d .miniconda ]; then
  echo "Conda not installed. Installing..."
  wget "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" -N -O ./miniconda.sh
  sh ./miniconda.sh -b -p ./.miniconda
  rm ./miniconda.sh
fi

export PATH="$(realpath ./.miniconda)/bin:$PATH"

if ! conda list | grep -q 'py312'; then
  echo "Conda Python 3.12 environment not found. Creating..."
  conda create -n py312 python=3.12 pip -y
fi

if [ ! -d .venv ]; then
  echo "VENV not found. Creating..."
  conda create -n py312 python=3.12 pip -y
  conda run -n py312 python -m venv .venv
fi

.venv/bin/python -m pip install -r requirements.txt --platform=manylinux2014_x86_64 --only-binary=:all: --target ./.venv/lib/python3.12/site-packages