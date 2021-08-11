import blue
import shared
import json

if __name__ == "__main__":
    resources = {
        'resource':
        shared.build() +
        blue.build()
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile,
                  sort_keys=True, indent=4)
