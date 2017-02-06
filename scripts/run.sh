#!/usr/bin/env bash

pushd "/usr/share/grafana-src/src/github.com/grafana/grafana"
go run build.go setup
go run build.go build
npm install
grunt
grunt watch &
bra run
popd