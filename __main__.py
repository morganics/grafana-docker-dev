import os
import subprocess
import urllib.parse

DOCKER_TLS_VERIFY="1"
DOCKER_HOST="tcp://192.168.99.100:2376"
DOCKER_MACHINE_NAME="grafana-dev1"
DOCKER_CERT_PATH=r"C:\Users\imorgan.admin\.docker\machine\machines\{}".format(DOCKER_MACHINE_NAME)
IMAGE_NAME = r"grafana-dev-image"

HOST_SHARE_FOLDER = r"C:\Users\imorgan.admin\share\grafana-src"

env = {'DOCKER_TLS_VERIFY': DOCKER_TLS_VERIFY,
       'DOCKER_HOST': DOCKER_HOST,
        'DOCKER_MACHINE_NAME': DOCKER_MACHINE_NAME,
        'DOCKER_CERT_PATH': DOCKER_CERT_PATH,
        'HOST_SHARE_FOLDER': HOST_SHARE_FOLDER,
       'IMAGE_NAME': IMAGE_NAME}

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

execute(delete_path, env)
execute(create_path, env)
set_docker_ip(env)
execute(init_path, env)
set_docker_ip(env)
execute(build_path, env)