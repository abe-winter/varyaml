import varyaml, pytest, itertools, os, yaml

os.environ['VY_KEY'] = 'hello'

def load(raw):
    "helper to dump & parse"
    return varyaml.load(yaml.dump(raw))

def test_dict():
    ret = load({'a':'$VY_KEY', 'b':1, 'c':'ok'})
    assert ret['a'] == os.environ['VY_KEY']
    assert ret['b'] == 1
    assert ret['c'] == 'ok'

def test_list():
    ret = load(['$VY_KEY', 1, 'ok'])
    assert ret[0] == os.environ['VY_KEY']
    assert ret[1] == 1
    assert ret[2] == 'ok'

def test_dict_default():
    assert 'X1' not in os.environ
    assert 'X3' not in os.environ
    os.environ['X0'] = '50'
    os.environ['X2'] = '60'
    ret = load({
        'omittable':'$X0', 'omitted':'$X1', 'present':'$X2', 'default':'$X3',
        'varyaml':{'defaults':{'X0':'__omit__', 'X1':'__omit__', 'X2':1, 'X3':1}},
    })
    assert ret['omittable'] == '50'
    assert 'omitted' not in ret
    assert ret['present'] == '60'
    assert ret['default'] == 1

def test_file_lookup():
    assert 'SECRET' not in os.environ
    ret = load({'fromfile':'$SECRET', 'varyaml':{'path':'.'}})
    assert ret['fromfile'] == 'secret-content\n'

def test_missing_error():
    "also test path here"
    assert 'MISSING' not in os.environ
    with pytest.raises(KeyError) as exc:
        load([{'missing':'$MISSING'}])
    assert exc.value.args == ('MISSING', '/0/missing')

def test_nest_cases():
    assert load({'a':{'b':'$VY_KEY'}})['a']['b'] == 'hello'
    assert load({'a':['$VY_KEY']})['a'][0] == 'hello'
    assert load([['$VY_KEY']])[0][0] == 'hello'
    assert load([{'b':'$VY_KEY'}])[0]['b'] == 'hello'
