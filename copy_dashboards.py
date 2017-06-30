token = "eyJrIjoiQXUwSHlDMDA4Y0NmVm9SdHRhT29TdW8wTWc3eWh4MXYiLCJuIjoiYW5wdGhlciIsImlkIjoxfQ=="

import getpass
import sdk
import boot2docker

DOCKER_MACHINE_NAME="grafana-dev4"
DOCKER_CERT_PATH=r"C:\Users\{}\.docker\machine\machines".format(getpass.getuser())
docker_machine = boot2docker.DockerMachine(DOCKER_MACHINE_NAME,
                                           boot2docker.VirtualBoxDriverCommands(),
                                           DOCKER_CERT_PATH)

ip = docker_machine.get_vm_ip()

path = r"C:\Users\{}\share\grafana-src\data\dashboards".format(getpass.getuser())
client = sdk.GrafanaClient(token, "http://{}:3000".format(ip))

for dashboard in client.dashboards().search("Hydro "):
    dashboard.rename(dashboard.title.replace("Hydro ", "Hydro MES "))
    dashboard.set_measurement('hydromes_turbines')
    #dashboard.save_to_file(path)
    #dashboard.push(overwrite=True)

