#!/usr/bin/env bash

pushd "/usr/share/grafana-src/src/github.com/grafana/grafana"
#go run build.go setup
#go run build.go build
npm install
grunt
grunt watch &

if [ ! -z "${GF_INSTALL_PLUGINS}" ]; then
  OLDIFS=$IFS
  IFS=','
  for plugin in ${GF_INSTALL_PLUGINS}; do
    IFS=$OLDIFS
    bin/grafana-cli --pluginsDir "data/plugins" plugins install ${plugin}
  done
fi

bra run
popd