import blue
import green
import passive
import shared
import json

if __name__ == "__main__":
    resources = {
        'resource':
        shared.build() +
        blue.build() +
        green.build()
        #  passive.build() +
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile,
                  sort_keys=True, indent=4)
