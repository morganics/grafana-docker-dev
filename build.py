import os
import subprocess
import urllib.parse
import getpass
import shutil
import sys
from boot2docker import client as b2d

docker_username = sys.argv[1]
docker_password = sys.argv[2]
docker_dev_repo = None
if len(sys.argv) > 4:
    docker_dev_repo = sys.argv[4]
docker_repo = sys.argv[3]

DOCKER_MACHINE_NAME="grafana-dev5"
DOCKER_CERT_PATH=r"C:\Users\{}\.docker\machine\machines".format(getpass.getuser())

DEV_IMAGE_NAME = r"grafana-dev-image"
HOST_SHARE_FOLDER = r"C:\Users\{}\share\grafana-src".format(getpass.getuser())
DEPLOY_IMAGE_NAME = "grafana_pub"

docker_machine = b2d.DockerMachine(DOCKER_MACHINE_NAME,
                                           b2d.VirtualBoxDriverCommands(),
                                           DOCKER_CERT_PATH)

docker = docker_machine.remove_local_env().create_local_env(HOST_SHARE_FOLDER, symlinks=True).get_docker_client()


## build the docker image
image = docker.build(DEV_IMAGE_NAME, dir="./dev-env")