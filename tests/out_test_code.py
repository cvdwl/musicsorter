test_args=("-v -v -j ~/projects/cruise/tests/data/test_code.json").split()
from example_pkg.config import project_config

def test_class_init():
    t = project_config(test_args=test_args)

def test_next():
    project = project_config(test_args=test_args)
    project.next()
    assert project.metadata['trial_acronym']=="MREP20"
    assert project['platform_type']=="drifter"
    assert project["spot_url"]=="https://api.findmespot.com"

from importlib import import_module
def test_read():
    project = project_config(test_args=test_args)
    project.next()
    processor = import_module(
         'example_pkg.{}_utils'.format(project['platform_type']))
    # process one platform
    processor.read_spot(project)

    assert project.metadata['trial_acronym']=="MREP20"
    assert project["spot_url"]=="https://api.findmespot.com"


