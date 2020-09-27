import credentials
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


def update_server(name, tags):
    driver = get_gce_driver()
    server = read_server(name)
    server = driver.ex_set_node_tags(node=node, tags=tags)
    return server


def delete_server(name):
    driver = get_gce_driver()
    server = read_server(name)
    server = driver.destroy_node(server)


if __name__ == "__main__":
    name = 'hello-world'
    try:
        server = read_server(name)
    except ResourceNotFoundError:
        server = create_server(name, 'ubuntu-1804-lts', 'f1-micro')
    print(server)

    # update_server(name, tags=["dev"])
    # delete_server(name)
