import yaml, os

class Omit: pass

class Settings:
    def __init__(self, settings):
        self.defaults = settings.get('defaults', {})
        self.path = settings.get('path')

    def substitute(self, var, path):
        if var in os.environ:
            return os.environ[var]
        elif self.path and os.path.exists(os.path.join(self.path, var)):
            return open(os.path.join(self.path, var)).read()
        elif var in self.defaults:
            return self.defaults[var]
        else:
            raise KeyError(var, path)

def process(item, settings, path=''):
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
            process(val, settings, '%s/%s' % (path, index))
        elif isinstance(val, str) and val.startswith('$'):
            newval = settings.substitute(val[1:], '%s/%s' % (path, index))
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
    settings = Settings(data.get('varyaml', {}) if isinstance(data, dict) else {})
    return process(data, settings)
