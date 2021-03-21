import io
import os
import re
import setuptools
    
# you may need to think about package_name versus package_folder.  In this 
# example, they're the same.
package_name="musicsorter"

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8
# some helper functions
def readme():
    ''' reads README and sends it I don't know where '''
    with io.open("README.md", encoding="utf-8") as f:
        return f.read()

def pip_requirements(fname="requirements.txt"):
    ''' grabs list of required packages from requirements.txt'''
    reqs = []
    for line in open(fname, "r"):
        reqs.append(re.sub('#.*$','',line.strip()))
    return [s for s in reqs if s]

def get_version():
    ''' Tries to get version info from VERSION.txt, updates with git tag,
    or assumes default.''' 
    try:
        with open(os.path.join(os.path.dirname(__file__),'VERSION.txt'),
                'r') as fh:
            version0 = fh.read()
    except:
        version0 = "0.0_uncommited"
    try:
        from git import Repo
        #repo = Repo(__file__,search_parent_directories=True)
        repo    = Repo('.git')
        isdirty = lambda x:"-dirty" if x.is_dirty() else ""
        tag     = repo.git.tag().split()[-1]
        commit  = f'{repo.head.commit.hexsha:.10s}{isdirty(repo)}'
        version = f'{tag}_{commit}_dev'
        if not tag == version0:
            with open(os.path.join(os.path.dirname(__file__),'VERSION.txt'),
                'w') as fh:
                fh.write(tag)
            repo.index.add('VERSION.txt')
    except:
        version = version0
    return version

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8
# Feed a bunch of hard-coded stuff to setuptools.  This can be much smarter
# and it's just python code.
setuptools.setup(

    # package name shows in conda listing
    name = package_name,

    # versioning
    version = get_version(),

    # Author info
    author = "Craig V. W. Lewis",
    author_email = "cvdwl at yahoo com",

    # some verbosity
    description = "Code demonstrating packaging",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    url = f"https://github.com/cvdwl/{package_name}",

    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS X",
    ],

    # find all the packages (from __init__.py?)
    packages = setuptools.find_namespace_packages(),

    # Specify python version this will work with
    python_requires = '>=3.6',

    # grab the list of requirements from a stupid text file
    install_requires = pip_requirements(),
    
    # direct pointer to a script
    scripts = [
        f'{package_name}/example_script.py',
    ],
    
    # these generate cmd line versions of internal functions.
    entry_points = {
        'console_scripts': [
            f'example_script = example_script:_example_script_main',
        ]
    },
    
    # make sure some data gets included.
    package_data = {
        f"{package_name}": [
            "data/*.*",
        ],
    },

    extras_require = {
        'testing' : ['pytest']
      },

    zip_safe = False
)
