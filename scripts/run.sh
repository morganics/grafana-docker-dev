#!/usr/bin/env bash

pushd "/usr/share/grafana-src/src/github.com/grafana/grafana"
exec go run build.go setup
exec go run build.go build
exec grunt
exec grunt watch
exec bra run
popd