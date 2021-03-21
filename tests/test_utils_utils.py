import os
from datetime import datetime as dtt

def test_mod_import_1():
    from example_pkg import abspth

def test_mod_import_2():
    from example_pkg import build_logger,nc2dtt

def check_dict_keys_strict( d, keys):
    return len(set(d.keys()) - set(keys)) == 0

def test_read_commented_json():
    # Check that it finds the file.
    from example_pkg import read_commented_json
    # is the test file there?
    J = read_commented_json(os.path.join(os.path.dirname(__file__),
                                         "data/test_good.json"))
    # is the data correct
    assert J["foo"] == "test_bar"
    # is the data complete
    assert check_dict_keys_strict(J, ["foo"]) 

def test_read_commented_json_bad():
    # Check that it finds the file.
    from example_pkg import read_commented_json
    # is the test file there?
    J = read_commented_json(os.path.join(os.path.dirname(__file__),
                                         "data/test_bad.json"))
    # is the data correct
    assert J["foo"] == "test_bar"
    # Make sure there's something else.
    assert not check_dict_keys_strict(J, ["foo"]) 
