import yaml, os

class Omit: pass

def substitute(var, defaults, path):
    if var in os.environ:
        # todo: do we want to support redirection here? see top-level README.md
        return os.environ[var]
    elif var in defaults:
        return defaults[var] == '__omit__'
    else:
        raise KeyError('%s not found (at %s)' % (var, path))

def process(item, defaults=None, path=''):
    "recursively processes containers. mutates input."
    iter_ = None
    if isinstance(item, dict):
        iter_ = dict.items()
    elif isinstance(item, list):
        iter_ = enumerate(item)
    else:
        return

    any_omit = False
    for index, val in iter_:
        if isinstance(val, (dict, list)):
            process(val, defaults, '%s/%s' % (path, index))
        elif isinstance(val, str) and val.startswith('$'):
            newval = substitute(val[1:], defaults, path+k+'/')
            if newval == '__omit__':
                if isinstance(item, list):
                    item[index] = Omit
                    any_omit = True
                elif isinstance(item, dict):
                    item.pop(index)

    if any_omit:
        assert isinstance(item, list)
        item[:] = (x for x in item if x is not Omit)

def load(*args, **kwargs):
    data = yaml.load(*args, **kwargs)
    defaults = d.get('varyaml') if isinstance(d, dict) else None
    return process(data, defaults)
