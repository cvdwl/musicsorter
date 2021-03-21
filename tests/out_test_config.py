import os
test_args="-vvv -j ~/projects/cruise/tests/data/test_cruise.json".split()

def test_pkg_import():
    from example_pkg.config import project_config
from example_pkg.config import project_config

def test_class_init():
    t = project_config(test_args=test_args)
    # check iteration
    assert t.next() == "scanfish"
    # check heritability
    assert t.platform['platform_type'] == 'scanfish'
    assert t['platform_type'] == 'scanfish'
    assert t['foo'] == 'bar'
    # some slightly different stuff
    assert t.next() == 'code'
    assert t['platform_type'] == 'drifter'
    assert t.next() is None
    assert t['platform_type'] is None

def test_buildpath():
    t = project_config(test_args=test_args)
    D = os.path.dirname(os.path.expanduser(test_args[-1]))
    assert t.build_path('/tmp/{project_name}') == '/tmp/MREP20'
    assert t.build_path(t["project_metadata"]) == \
        os.path.join(D,"json/MREP20_metadata.json")

def test_metadata():
    t = project_config(test_args=test_args)
    assert t.project_metadata['trial_name'] == 'MREP20'
    t.next()
    assert t.metadata['ship'] == 'ITN Alliance'
    assert t.metadata['test_scanfish_metadata'] == 'test_metadata_value'
    t.next()
    assert t.metadata['ship'] == 'NRV Alliance'

