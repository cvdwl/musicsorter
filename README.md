# packaging_tutorial

Trying to figure out how to package python code.  Hacked up to handle a
variety of cases, including in-line data

Derived from
[python.org](https://packaging.python.org/tutorials/packaging-projects)
examples.

# Installation

This works:

`pip install git+http://github.com/cvdwl/example_pkg.git`

Also:

`pip install git+ssh://git@github.com/cvdwl/example_pkg.git`

Note that you'll need to do a develop install before commit:

`pip install -e .`

in order to allow `setup.py` to update `VERSION.txt`.

# Running Tests

## Prerequisites.

If you install this with the `testing` feature (`pip install .[testing]`),
then pytest will automatically be installed. You can also just install it
with `pip install pytest`.

## Running Tests.

You can then run pytest from the command line, and it will try and find tests:

```
$ pytest
```

# Examples

This is a simple example package. You can use
[Github-flavored Markdown](
https://guides.github.com/features/mastering-markdown/)
to write your content.

PyPa [sample](https://github.com/pypa/sampleproject.git)

Cimino [repo](https://github.com/gpcimino/pytemplate.git)
