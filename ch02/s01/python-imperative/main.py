import credentials
from pprint import pprint
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.common.google import ResourceNotFoundError


def get_gce_driver():
    driver = get_driver(Provider.GCE)(
        credentials.GOOGLE_SERVICE_ACCOUNT_EMAIL,
        credentials.GOOGLE_SERVICE_ACCOUNT_KEY_FILE,
        project=credentials.GOOGLE_PROJECT,
        datacenter=credentials.GOOGLE_ZONE)
    return driver


def create_server(name, image_family, size):
    driver = get_gce_driver()
    image = driver.ex_get_image_from_family(image_family)
    server = driver.create_node(name=name, image=image, size=size)
    return server


def read_server(name):
    driver = get_gce_driver()
    server = driver.ex_get_node(name=name)
    return server


def update_server_mutable(name, labels={}):
    driver = get_gce_driver()
    server = read_server(name)
    status = driver.ex_set_node_labels(server, labels)
    return status

def update_server_immutable(name, image_family=None):
    server = read_server(name)
    delete_server(name)
    server = create_server(name, image_family, server.size)
    return server


def delete_server(name):
    driver = get_gce_driver()
    server = read_server(name)
    status = driver.destroy_node(server)
    return status


def change_image(image_family):
    driver = get_gce_driver()
    server = read_server(name)
    new_image = driver.ex_get_image_from_family(image_family)
    return new_image.name is not server.image


def change_labels(labels):
    server = read_server(name)
    return labels != server.extra['labels']

if __name__ == "__main__":
    name = 'hello-world'
    image = 'ubuntu-2004-lts'
    machine_type = 'f1-micro'
    labels = {'environment':'dev'}

    try:
        server = read_server(name)
    except ResourceNotFoundError:
        server = create_server(name, image, machine_type)

    server = read_server(name)
    print('Server parameters after update: ' +
          str(server.extra['labels']) + ' , ' + server.image)

    if change_image(image):
        update_server_immutable(name, image)

    server = read_server(name)
    print('Server parameters after update: ' +
          str(server.extra['labels']) + ' , ' + server.image)

    if change_labels(labels):
        update_server_mutable(name, labels)

    server = read_server(name)
    print('Server parameters after update: ' +
          str(server.extra['labels']) + ' , ' + server.image)

    delete_server(name)
