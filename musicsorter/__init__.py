import logging
import json
import copy
import os
import re
import sys

import numpy as np

from collections import OrderedDict

from datetime import datetime as dtt
from datetime import timedelta as tdt
from datetime import timezone as dtz

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8


abspth = lambda *x:os.path.abspath(os.path.expanduser(os.path.join(*x)))

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8

# return a pathname with the $HOME converted to "~"
def fnr(fn,root='~',rootreplacement='~'):
    return re.sub(os.path.expanduser(root),rootreplacement,fn)

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8

# returns all keys of a format string
def get_format_keys(f):
    return [i.strip('{}').split(':')[0] for i in
            list(np.unique(re.findall(r"\{[A-Za-z0-9_:]+\}", f)))]

# Make a path for a file
def makepath(dirname,isfile=True):
    if isfile:
        dirname = os.path.dirname(dirname)
    if not os.path.isdir(dirname):
        import pathlib
        logger = logging.getLogger("cruise.makepath")
        logger.warning('CREATING PATH: {}'.format(dirname))
        pathlib.Path(os.path.expanduser(dirname)).mkdir(
                parents=True, exist_ok=True)

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8
# merge or insert a key into a dictionary, creating subentries as needed.
# CVL note: this isn't bulletproof!

def dictaddmerge(d,k,v,s=' '):
    listtypes = [list]
    if not k in d.keys():
        d[k] = v
    else:
        if type(d[k]) in listtypes and type(v) in listtypes:
            d[k] = d[k] + v
        if type(d[k]) in listtypes and not type(v) in listtypes:
            d[k].append(v)
        if type(d[k]) == str:
            d[k] = s.join([d[k],v])
        if type(v) == dict:
            for kv in v.keys():
                logger = logging.getLogger("cruise.dictaddmerge")
                logger.debug("  *** hang on, we're going recursive! ***")
                d[k] = dictaddmerge(d[k],kv,v[kv])
    return d

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8
# 
# User and repo parameters

# GIT info
def git_info():
    logger = logging.getLogger()
    try:
        from git import Repo,InvalidGitRepositoryError
    except (ImportError, ModuleNotFoundError):
        logger.warning('No git python support')
        return {}
    # Split out repo processing from import
    try:
        isdirty = lambda x:"(dirty)" if x.is_dirty else ""
        repo = Repo(__file__,search_parent_directories=True)
        return {
             'version':repo.git.tag().split()[-1],
             'commit':f'{repo.head.commit.hexsha:.10s}{isdirty(repo)}',
             'remote':repo.remote(repo.remotes[0]).url,
             }
    except (InvalidGitRepositoryError,ValueError):
        logger.warning('Invalid git repo issues')
    except Exception as ex:
        template = "UNCAUGHT EXCEPTION: {0} - Arguments:\n{1!r}\n"
        message = template.format(type(ex).__name__, ex.args)
        logger.warning(message)
    return {}

# a string showing how program was invoked
def get_program_invocation():
    return ' '.join([os.path.basename(sys.argv[0])] +
                    [i if not ' ' in i else '"{}"'.format(i)
                     for i in sys.argv[1:]])

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8
#
#

def nc2dtt(t,u,**kwargs):
    return netCDF4.num2date(t,u,**kwargs,
                            only_use_python_datetimes=True,
                            only_use_cftime_datetimes=False)

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8
#
def read_commented_json(filename,encoding='ISO-8859-1'):
    """ reads a json file, stripping comments beginning with // """
    with open(filename,'r',encoding=encoding) as fh:
        return json.loads(
            re.sub('(?<!:)//.*\n', '',fh.read()),
            object_pairs_hook = OrderedDict )

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8
#
# Build a logger instance based on options.

def build_logger(logger=None,opts=[],name='logger',loglevel = logging.DEBUG):

    logger = logger or logging.getLogger(name)

    # choose logging level based on toptions
    if opts:
        loglevel = [logging.ERROR,
                    logging.WARNING,
                    logging.INFO,
                    logging.DEBUG][
                        max(0,min(3,opts.verbose-opts.quiet+1))]
    logger.setLevel(loglevel)
    ch = logging.StreamHandler(sys.stdout)
    logger.handlers=[]
    # use verbose formatting for debug logging
    if logger.getEffectiveLevel() < logging.INFO:
        formatter = logging.Formatter(
            '%(levelname).3s-%(name)s: %(message)s')
    else:
        formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.debug('loglevel: {}'.format(logger.getEffectiveLevel()))
    return logger

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8

def duplicate_netcdf(infile=None,outfile=None,copy_data=True):
    '''
    Create a duplicate netcdf file.  Optionally do not copy data.
    '''
    try:os.remove(outfile)
    except:pass
    with netCDF4.Dataset(infile,'r') as nci, \
         netCDF4.Dataset(outfile,'w') as nco:
        for d in nci.dimensions:
            nco.createDimension(d,nci.dimensions[d].size)
        for v in nci.variables:
            nco.createVariable(v,datatype=nci[v].datatype,
                           dimensions= nci[v].dimensions)
            nco[v].setncatts({
                a:nci[v].getncattr(a) for a in nci[v].ncattrs()
                if not a.startswith('_')
            })
            if copy_data:
                nco[v][:] = nci[v][:]
        nco.setncatts({
            a:nci.getncattr(a) for a in nci.ncattrs()
        })
    return outfile

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8

def get_json(filename ,
             json_content = False, ):
    '''
    Read a json file respecting the \\comment convention.
    '''
    logger = logging.getLogger('cruise.get_json')
    filename = os.path.abspath(os.path.expanduser(filename))

    # Handle mutability issues!!!
    if not json_content:
        json_content = OrderedDict({})
    try:
        logger.debug('  reading json file: {}'.format(
            fnr(filename)))
        with open(filename,'r',encoding='ISO-8859-1') as equipFileHandle:
            tmpConfig = json.loads(
                re.sub('(?<!:)//.*\n', '',equipFileHandle.read()),
                object_pairs_hook = OrderedDict )
        json_content.update(tmpConfig)
    except IOError:
        logger.warning('  *** json file: {} NOT FOUND'.format(
            filename))
    except ValueError:
        logger.warning('  *** json file: {} NOT READABLE'.format(
            filename))
    except Exception as ex:
        template = "  UNCAUGHT EXCEPTION: {0} - Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logger.warning(message)
    return copy.deepcopy(json_content)
