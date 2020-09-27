try:
    import secrets
except ImportError:
    print('"demos/secrets.py" not found.\n\n'
          'Please copy secrets.py-dist to secrets.py and update the GCE* '
          'values with appropriate authentication information.\n')
    sys.exit(1)

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

args = getattr(secrets, 'GCE_PARAMS', ())
kwargs = getattr(secrets, 'GCE_KEYWORD_PARAMS', {})


def get_gce_driver():
    driver = get_driver(Provider.GCE)(*args, **kwargs)
    return driver


def create_server(name, image_family, size):
    driver = get_gce_driver()
    image = driver.ex_get_image_from_family(image_family)
    node = driver.create_node(name=name, image=image, size=size)
    return node


def read_server(name):
    driver = get_gce_driver()
    node = driver.ex_get_node(name=name)
    return node


def update_server(name, tags):
    driver = get_gce_driver()
    node = read_server(name)
    node = driver.ex_set_node_tags(node=node, tags=tags)
    return node

def delete_server(name):
    driver = get_gce_driver()
    node = read_server(name)
    node = driver.destroy_node(node)


if __name__ == "__main__":
    name = 'hello-world'
    #create_server(name, 'ubuntu-1804-lts', 'f1-micro')
    update_server(name, tags=["dev"])
    delete_server(name)

