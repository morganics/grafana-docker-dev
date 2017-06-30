#!/usr/bin/env bash

pushd "/usr/share/grafana-src/src/github.com/grafana/grafana"

# remove non-windows line endings
find . -type f -print0 | xargs -0 -n 1 -P 4 dos2unix

go run build.go build pkg-deb
popd