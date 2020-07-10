import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here


@pytest.fixture(scope='session')
def dd_environment():

    compose_file = os.path.join(get_here(), 'docker', 'docker-compose.yml')

    KERNELCARE_KEY = 'KernelCareKey'
    URL = 'http://{}:8000/'.format(get_docker_hostname())
    endpoint = URL + KERNELCARE_KEY

    with docker_run(compose_file, endpoints=[endpoint]):
        yield {'KERNELCARE_KEY': KERNELCARE_KEY, 'URL': URL}
