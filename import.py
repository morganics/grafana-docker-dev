token = "eyJrIjoiNUV2U040M0xIaGRLcWFtTDBJU2VRN1Z0SExVUWVQSEQiLCJuIjoicHl0aG9uIiwiaWQiOjF9"
remote_token = "eyJrIjoiTkF3N1FwQlVJM1p1cml1SEE4V0N5MnlCNUFyWTdaWlIiLCJuIjoiZWRpdG9yIiwiaWQiOjF9"
import getpass
import sdk

from boot2docker import client as b2d
DOCKER_MACHINE_NAME="grafana-dev5"
DOCKER_CERT_PATH=r"C:\Users\{}\.docker\machine\machines".format(getpass.getuser())
docker_machine = b2d.DockerMachine(DOCKER_MACHINE_NAME,
                                           b2d.VirtualBoxDriverCommands(),
                                           DOCKER_CERT_PATH)

ip = docker_machine.get_vm_ip()

path = r"C:\Users\{}\share\grafana-src\data\dashboards".format(getpass.getuser())
client = sdk.GrafanaClient(token, "http://{}:3000".format(ip))

remote_client = sdk.GrafanaClient(remote_token, "http://ec2-34-197-128-68.compute-1.amazonaws.com:3000")

datasource = client.datasources().get('turbine')
print(datasource._fields)

for dashboard in remote_client.dashboards().search("DEMO"):
    dashboard.save_to_file(path)
    dashboard.push(client, overwrite=True)

