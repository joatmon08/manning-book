import cluster
import json

if __name__ == "__main__":
    resources = {
        'resource': cluster.build()
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile,
                  sort_keys=True, indent=4)
