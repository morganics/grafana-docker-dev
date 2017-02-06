# grafana-docker-dev
For setting up the grafana environment in docker and developing in a windows host (via boot2docker). Nothing too clever, when running from 
\_\_main\_\_ sets up a virtual box with symlinks, and links the environment to a shared folder on your windows host. Could be run with a unix host as well with a few small modifications.

Assumes that you have a checked out version of the grafana source code on your shared location.

Steps are:

1. Build the boot2docker VM environment (docker_delete, docker_create, docker_init_share)
2. Build the Dockerfile image on the selected VM (docker_build)
3. Run the resulting docker image using:

        docker run -it -p 3000:3000 --rm --volume /Users:/usr/share/grafana-src/src/github.com/grafana/grafana \
            --name grafana-dev grafana-dev-image
        
   This will run npm build, the Grafana setup scripts, build and install, ```grunt watch``` and ```bra run```. You can then edit your local copy of Grafana and the running container should update accordingly, so you should then be able to view any changes (fairly) immediately in your browser.
   
4. When you want to deploy, you can attach another session to the running container: ```docker exec -it grafana-dev /bin/bash```. Then change directory ```cd src/github.com/grafana/grafana``` and finally run ```go run build.go build package```. This will generate the deb package.
5. Finally, you can run the last step in \_\_main\_\_ (deploy_docker_build, docker_push and docker_login)   
