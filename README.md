# grafana-docker-dev
For setting up the grafana environment in docker and developing in a windows host (via boot2docker). Nothing too clever, when running from 
__main__ sets up a virtual box with symlinks, and links the environment to a shared folder on your windows host. Could be run with a unix
host as well with a few small modifications.

Assumes that you have a checked out version of the grafana source code on your shared location.

To run the docker image:

    docker run -it -p 3000:3000 --rm --volume /Users:/usr/share/grafana-src/src/github.com/grafana/grafana \
        --name grafana-dev grafana-dev-image /bin/bash
       
