import yaml, os

class Omit: pass

def substitute(var, defaults, path):
    if var in os.environ:
        # todo: do we want to support redirection here? see top-level README.md
        return os.environ[var]
    elif defaults and var in defaults:
        return defaults[var]
    else:
        raise KeyError(var, path)

def process(item, defaults=None, path=''):
    "recursively processes containers. mutates input."
    iter_ = None
    if isinstance(item, dict):
        iter_ = item.items()
    elif isinstance(item, list):
        iter_ = enumerate(item)
    else:
        return item

    any_omit = False
    pops = []
    for index, val in iter_:
        if isinstance(val, (dict, list)):
            process(val, defaults, '%s/%s' % (path, index))
        elif isinstance(val, str) and val.startswith('$'):
            newval = substitute(val[1:], defaults, '%s/%s' % (path, index))
            if newval == '__omit__':
                if isinstance(item, list):
                    item[index] = Omit
                    any_omit = True
                elif isinstance(item, dict):
                    pops.append(index)
            else:
                item[index] = newval

    if pops:
        assert isinstance(item, dict)
        for k in pops:
            item.pop(k)
    if any_omit:
        assert isinstance(item, list)
        item[:] = (x for x in item if x is not Omit)

    return item

def load(*args, **kwargs):
    data = yaml.load(*args, **kwargs)
    defaults = data.get('varyaml') if isinstance(data, dict) else None
    return process(data, defaults)
