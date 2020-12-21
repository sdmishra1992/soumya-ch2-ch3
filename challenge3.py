import json

def nested_key(object, key):
    key_val = key.split('/')
    obj = json.loads(object)
    nest_key = dict()
    nest_dict = None
    for i in key_val:
        try:
            nest_key = obj[i]
        except KeyError:
            pass
        json_key = json.loads(json.dumps(nest_key))
        for s, e in json_key.items():
            nest_dict = e

    return nest_dict['{}'.format(key_val[len(key_val) -1])]


object = '{"x":{"y":{"z":"a"}}}'
key = 'x/y/z'

print(nested_key(object, key))
