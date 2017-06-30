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
dist_deb_path = r"C:\Users\{}\share\grafana-src\dist".format(getpass.getuser())

docker_machine = b2d.DockerMachine(DOCKER_MACHINE_NAME,
                                           b2d.VirtualBoxDriverCommands(),
                                           DOCKER_CERT_PATH)

if not docker_machine.vm_exists():
    docker_machine.create_local_env(HOST_SHARE_FOLDER)

docker_machine.vm_regenerate_certs()

if docker_machine.vm_status_stopped():
    docker_machine.vm_start()

docker = docker_machine.get_docker_client()

image = docker.get_image(DEV_IMAGE_NAME)
#image.get_container("grafana-dev").stop().remove()
#image.get_container("grafana-dev-deploy").stop().remove()

# build the .deb using another entrypoint.
image.run(port_map=(3000, 3000),
              volume=("/Users", "/usr/share/grafana-src/src/github.com/grafana/grafana"),
              container_name="grafana-dev-deploy",
              entrypoint="./build.sh")

## DEPLOY:
## Need to build the docker image inside the container, so stop the server ^^
## and restart with a bin/bash entrypoint:
#image.run(port_map=(3000, 3000),
#          volume=("/Users", "/usr/share/grafana-src/src/github.com/grafana/grafana"),
#          container_name="grafana-dev")
# docker run -it -p 3000:3000 --rm --volume /Users:/usr/share/grafana-src/src/github.com/grafana/grafana --entrypoint /bin/bash --name grafana-dev grafana-dev-image
## and inside the container
# cd src/github.com/grafana/grafana
# go run build.go build package
for file in [f for f in os.listdir(dist_deb_path) if f.endswith('.deb')]:
    shutil.copyfile(os.path.join(dist_deb_path, file), "deploy-env/grafana.deb")

docker.login(docker_username, docker_password)

image = docker.build(DEPLOY_IMAGE_NAME, tag='latest', dir='deploy-env')
#image.get_container("grafana-test").stop().remove()
#image.run(port_map=(3000, 3000),
#              volume=("/Users", "/usr/share/grafana-src/src/github.com/grafana/grafana"),
#              container_name="grafana-test", remove=False)
image.tag(docker_repo)
image.push(docker_repo)

# deploy_build_path = os.path.join("deploy", "docker_build.cmd")
# docker_push_path = os.path.join("deploy", "docker_push.cmd")
# docker_login_path = os.path.join("deploy", "docker_login.cmd")
#
# shutil.copyfile(dist_deb_path, "deploy/grafana.deb")
#
# set_docker_ip(env)
# execute(deploy_build_path, env)
# execute(docker_login_path, env)
# execute(docker_push_path, env)
