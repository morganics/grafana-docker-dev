import requests
import os
import json
from typing import Iterator
import collections


class GrafanaClient:

    def __init__(self, token, url):
        self._token = token
        self.url = url

    def datasources(self) -> 'DataSources':
        return DataSources(self)

    def dashboards(self) -> 'Dashboards':
        return Dashboards(self)

    def auth(self):
        return {'Authorization': "Bearer {}".format(self._token)}

    def headers(self):
        return {**{"Accept": "application/json", "Content-Type": "application/json"}, **self.auth()}


class Dashboard:

    def __init__(self, client, id, title, url, content):
        self.url = url
        self.title = title
        self.id = id
        self._client = client
        self.content = content

    def save_to_file(self, path):
        with open(os.path.join(path, self.title.replace(" ", "_")) + ".json", "w") as fh:
            json.dump(self.content['dashboard'], fh)

    def rename(self, title):
        self.title = title
        self.content['dashboard']['title'] = title

    @staticmethod
    def _update(k, v, u):
        ret = {}
        for key, val in u.items():
            if isinstance(val, collections.Mapping):
                r = Dashboard._update(k, v, val)
                ret[key] = r
            else:
                if key == k:
                    ret[key] = v
                else:
                    ret[key] = u[key]
        return ret

    def set_measurement(self, measurement):
        self.content = Dashboard._update('measurement', measurement, self.content)

    def push(self, remote_client: 'GrafanaClient'=None, overwrite=True):

        if remote_client is None:
            remote_client = self._client

        self.content['dashboard'].pop('id', None)

        params = {'overwrite': overwrite,
                  'dashboard': self.content['dashboard']}

        response = requests.post(remote_client.url + "/api/dashboards/db",
                    data=json.dumps(params),
                    headers=remote_client.headers())

        print(response.content)


class Dashboards:

    def __init__(self, client: GrafanaClient):
        self._client = client

    def search(self, query) -> Iterator[Dashboard]:
        response = requests.get(self._client.url + "/api/search", params={
            'query': query
        }, headers=self._client.headers())

        if response.ok:
            info = json.loads(response.content.decode("utf-8") )
            for d in info:
                yield Dashboard(self._client, d['id'], d['title'], d['uri'], self.get(d['uri']))


    def get(self, uri):
        response = requests.get(self._client.url + "/api/dashboards/{}".format(uri),
                                headers=self._client.headers())

        return json.loads(response.content.decode('utf-8'))

class DataSources:

    def __init__(self, client):
        self._client = client

    def get(self, name) -> 'DataSource':
        response = requests.get(self._client.url + "/api/datasources/id/3".format(name),
                                headers=self._client.headers())
        fields = json.loads(response.content.decode('utf-8'))

        return DataSource(fields)


class DataSource:

    def __init__(self, fields):
        self._fields = fields

    def push(self, remote_client: 'GrafanaClient', overwrite=True):

        params = self._fields

        response = requests.post(remote_client.url + "/api/datasources",
                                 data=json.dumps(params),
                                 headers=remote_client.headers())

        print(response.content)




