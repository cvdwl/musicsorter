
def test_mod_import():
  from example_pkg import foo as foo

def check_dict_keys_strict( d, keys):
  return len(set(d.keys()) - set(keys)) == 0

def test_bar():
  from example_pkg import foo as foo
  J = foo.bar()
  assert J["foo"] == "bar"
  assert check_dict_keys_strict(J, ["foo"]) # Make sure there's nothing else.

def test_bar_reader():
  # Check that it finds the file.
  from example_pkg import foo as foo
  import os
  J = foo.bar_(os.path.join(os.path.dirname(__file__), "data/test_good.json"))

def test_bar_reader_good():
  # Check that the data looks right.
  from example_pkg import foo as foo
  import os
  J = foo.bar_(os.path.join(os.path.dirname(__file__), "data/test_good.json"))

  assert J["foo"] == "test_bar"
  assert check_dict_keys_strict(J, ["foo"]) # Make sure there's nothing else.

def test_bar_reader_bad():
  from example_pkg import foo as foo
  import os
  J = foo.bar_(os.path.join(os.path.dirname(__file__), "data/test_bad.json"))

  assert not check_dict_keys_strict(J, ["foo"]) # Make sure there's something else.
