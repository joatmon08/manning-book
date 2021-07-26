import blue
import green
import database
import passive
import shared
import json

if __name__ == "__main__":
    resources = {
        'resource':
        shared.build() +
        blue.build() +
        green.build() + 
        database.build()
        #  passive.build() +
    }

    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile,
                  sort_keys=True, indent=4)
