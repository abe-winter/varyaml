import yaml, os

class Omit: pass

def get_overrides(settings):
    "takes the varyaml section of a conf and the passed-in tags; returns matched override section or {}"
    overrides = settings.get('overrides', [])
    for section in overrides:
        assert '__filter__' in section
        if any(os.environ.get(key) == val for key, val in section['__filter__'].items()):
            return section
    return {}

class Settings:
    "some kind of helper to manage interpolation & precedence"
    def __init__(self, settings):
        self.defaults = settings.get('defaults', {})
        self.overrides = get_overrides(settings)
        self.path = settings.get('path')

    def substitute(self, var, path):
        if var in os.environ:
            return os.environ[var]
        elif self.path and os.path.exists(os.path.join(self.path, var)):
            return open(os.path.join(self.path, var)).read()
        elif var in self.overrides:
            return self.overrides[var]
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
    data = yaml.safe_load(*args, **kwargs)
    settings = Settings(data.get('varyaml', {}) if isinstance(data, dict) else {})
    return process(data, settings)
