import blue
import green
import passive
import shared
import json

if __name__ == "__main__":
    resources = {'resource': blue.build() +
                 passive.build() + shared.build() +
                 green.build()}

    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile,
                  sort_keys=True, indent=4)
