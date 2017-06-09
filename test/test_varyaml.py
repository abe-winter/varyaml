import varyaml, pytest, itertools, os, yaml

os.environ['VY_KEY'] = 'hello'

def test_dict():
    ret = varyaml.load(yaml.dump({'a':'$VY_KEY', 'b':1, 'c':'ok'}))
    assert ret['a'] == os.environ['VY_KEY']
    assert ret['b'] == 1
    assert ret['c'] == 'ok'

def test_list():
    ret = varyaml.load(yaml.dump(['$VY_KEY', 1, 'ok']))
    assert ret[0] == os.environ['VY_KEY']
    assert ret[1] == 1
    assert ret[2] == 'ok'

def test_omit_dict():
    raise NotImplementedError

def test_omit_list():
    raise NotImplementedError

def test_missing_error():
    "also test path here"
    raise NotImplementedError

@pytest.mark.parametrize('t1,t2', itertools.product((list, dict), (list, dict)))
def test_nest_cases(t1, t2):
    raise NotImplementedError
