import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here


@pytest.fixture(scope='session')
def dd_environment():

    compose_file = os.path.join(get_here(), 'docker', 'docker-compose.yml')

    KEY_OK = 'KernelCareKey'
    KEY_FAIL = 'NotFoundKey'
    URL = 'http://{}:8000/'.format(get_docker_hostname())
    endpoints = [URL + KEY_OK, URL + KEY_FAIL]

    with docker_run(compose_file, endpoints=endpoints):
        yield {'KEY_OK': KEY_OK, 'KEY_FAIL': KEY_FAIL, 'URL': URL}
