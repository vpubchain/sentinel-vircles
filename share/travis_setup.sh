#!/bin/bash
set -evx

mkdir ~/.virclescore

# safety check
if [ ! -f ~/.virclescore/.vircles.conf ]; then
  cp share/vircles.conf.example ~/.virclescore/vircles.conf
fi
