#!/usr/bin/env python

import requests
import json

def load():
    meta_url = 'http://169.254.169.254/latest'
    meta_values = {'dynamic': {}, 'meta-data': {}, 'user-data': {}}

    for val in meta_values.keys():
        datacrawl('{0}/{1}/'.format(meta_url, val), meta_values[val])

    return meta_values


def datacrawl(url, op):
    r = requests.get(url)
    if r.status_code == 404:
        return

    for l in r.text.split('\n'):
        if not l: # "instance-identity/\n" case
            continue
        newurl = '{0}{1}'.format(url, l)
        # a key is detected with a final '/'
        if l.endswith('/'):
            newkey = l.split('/')[-2]
            op[newkey] = {}
            datacrawl(newurl, op[newkey])

        else:
            r = requests.get(newurl)
            if r.status_code != 404:
                try:
                    op[l] = json.loads(r.text)
                except ValueError:
                    op[l] = r.text
            else:
                op[l] = None
                

def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


if __name__ == '__main__':
    json_data = json.dumps(load())
    json_file = open('/tmp/file.json','w+')
    json_file.write(json_data)
    json_obj = json.loads(json_data)
    print(json_extract(json_obj,'instance-id'))
