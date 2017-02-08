import os
import subprocess
import urllib.parse
import getpass
import shutil
import sys

docker_username = sys.argv[1]
docker_password = sys.argv[2]
docker_repo = sys.argv[3]

DOCKER_TLS_VERIFY="1"
DOCKER_HOST="tcp://192.168.99.100:2376"
DOCKER_MACHINE_NAME="grafana-dev1"
DOCKER_CERT_PATH=r"C:\Users\{}\.docker\machine\machines\{}".format(getpass.getuser(), DOCKER_MACHINE_NAME)
IMAGE_NAME = r"grafana-dev-image"
HOST_SHARE_FOLDER = r"C:\Users\{}\share\grafana-src".format(getpass.getuser())
DEPLOY_IMAGE_NAME = "grafana_pub"
dist_deb_path = r"C:\Users\{}\share\grafana-src\dist\grafana_4.2.0-1486135758pre1_amd64.deb".format(getpass.getuser())

env = {'DOCKER_TLS_VERIFY': DOCKER_TLS_VERIFY,
       'DOCKER_HOST': DOCKER_HOST,
        'DOCKER_MACHINE_NAME': DOCKER_MACHINE_NAME,
        'DOCKER_CERT_PATH': DOCKER_CERT_PATH,
        'HOST_SHARE_FOLDER': HOST_SHARE_FOLDER,
       'IMAGE_NAME': IMAGE_NAME,
       'DOCKER_REPO': docker_repo,
       'DEPLOY_IMAGE_NAME': DEPLOY_IMAGE_NAME,
       'DOCKER_USERNAME': docker_username,
       'DOCKER_PASSWORD': docker_password
       }

def execute(path, env):
    p = subprocess.Popen(os.path.basename(path), cwd=os.path.dirname(path), env={**os.environ, **env}, shell=True)
    out, err = p.communicate()
    return p.returncode, out, err

def get_docker_ip(env):
    out = subprocess.check_output("docker-machine ip {}".format(env['DOCKER_MACHINE_NAME']), env={**os.environ, **env}, shell=True)
    subprocess.call("docker-machine regenerate-certs -f {}".format(env['DOCKER_MACHINE_NAME']), env={**os.environ, **env}, shell=True)
    return out.decode("utf-8").strip()

def set_docker_ip(env):
    ip = get_docker_ip(env)
    p = urllib.parse.urlparse(env['DOCKER_HOST'])
    env['DOCKER_HOST'] = "{}://{}:{}".format(p.scheme, ip, p.port)

delete_path = os.path.join("scripts", "docker_delete.cmd")
create_path = os.path.join("scripts", "docker_create.cmd")
init_path = os.path.join("scripts", "docker_init_share.cmd")
build_path = os.path.join("scripts", "docker_build.cmd")

## Remove any existing boot2docker vm
#execute(delete_path, env)

## Create the boot2docker vm
#execute(create_path, env)

## get the IP of the boot2docker vm
#set_docker_ip(env)

## Setup the shared folder
#execute(init_path, env)
set_docker_ip(env)

## build the docker image
#execute(build_path, env)

## DEPLOY:

## Need to build the docker image inside the container, so stop the server ^^
## and restart with a bin/bash entrypoint:
# docker run -it -p 3000:3000 --rm --volume /Users:/usr/share/grafana-src/src/github.com/grafana/grafana --entrypoint /bin/bash --name grafana-dev grafana-dev-image
## and inside the container
# cd src/github.com/grafana/grafana
# go run build.go build package

deploy_build_path = os.path.join("deploy", "docker_build.cmd")
docker_push_path = os.path.join("deploy", "docker_push.cmd")
docker_login_path = os.path.join("deploy", "docker_login.cmd")

shutil.copyfile(dist_deb_path, "deploy/grafana.deb")

set_docker_ip(env)
execute(deploy_build_path, env)
execute(docker_login_path, env)
execute(docker_push_path, env)
