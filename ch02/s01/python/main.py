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


def update_server(name, image_family=None, labels={}):
    driver = get_gce_driver()
    server = read_server(name)
    if image_family is not None:
        new_image = driver.ex_get_image_from_family(image_family)
        if new_image.name is not server.image:
            delete_server(name)
            server = create_server(name, image_family, server.size)
    status = driver.ex_set_node_labels(server, labels)
    return status


def delete_server(name):
    driver = get_gce_driver()
    server = read_server(name)
    status = driver.destroy_node(server)
    return status


if __name__ == "__main__":
    name = 'hello-world'
    try:
        server = read_server(name)
    except ResourceNotFoundError:
        server = create_server(name, 'ubuntu-1804-lts', 'f1-micro')
    print('Server parameters after creation: ' +
          str(server.extra['labels']) + ' , ' + server.image)

    if not update_server(name, image_family='ubuntu-2004-lts',
                         labels={"environment": "dev"}):
        raise Exception("Update to server failed")

    server = read_server(name)
    print('Server parameters after update: ' +
          str(server.extra['labels']) + ' , ' + server.image)

    delete_server(name)
